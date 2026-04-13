#!/usr/bin/env python3
"""
Скрипт массового обновления Django-сайтов (food) на серверах Beget.

Для каждого сайта из конфигурации:
1. Инициализирует git и подтягивает origin/main
2. Устанавливает/обновляет зависимости (pip install)
3. Генерирует и применяет Django-миграции (makemigrations + migrate)
4. Собирает статические файлы (collectstatic)
5. Перезапускает Passenger
6. Проверяет HTTP-доступность (код 200)
7. Проверяет актуальность кода (HEAD == origin/main)

Django-команды выполняются через ssh localhost -p222 (Docker-окружение Beget).
Git-операции — через обычный SSH.

Требования:
- sshpass на локальной машине (sudo apt-get install sshpass)
- SSH-доступ к серверам (пароль в конфигурации)
- git на серверах

Использование:
  python3 update_sites.py --config update_config.json          # обновить все
  python3 update_sites.py --config update_config.json -s site1 # обновить один
  python3 update_sites.py --config update_config.json --check  # только проверка
  python3 update_sites.py --config update_config.json --list   # список сайтов
  python3 update_sites.py --config update_config.json --dry-run # тестовый прогон
"""

import json
import os
import sys
import subprocess
import base64
from datetime import datetime
import argparse
import urllib.request
import ssl
import time


class SiteUpdater:
    def __init__(self, config_path, dry_run=False):
        self.config = self._load_config(config_path)
        self.dry_run = dry_run
        self.log_file = f"update_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.git_repo = self.config.get('git_repo', 'https://github.com/Gorills/food.git')
        self.git_branch = self.config.get('git_branch', 'main')
        self.docker_port = self.config.get('docker_port', 222)
        self.results = {}
        self._check_requirements()

    def _load_config(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Файл конфигурации не найден: {path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Ошибка JSON в {path}: {e}")
            sys.exit(1)

    def _check_requirements(self):
        tools = ['ssh', 'git']
        if not self.dry_run:
            tools.append('sshpass')
        missing = []
        for tool in tools:
            try:
                subprocess.run(['which', tool], capture_output=True, check=True)
            except subprocess.CalledProcessError:
                missing.append(tool)
        if missing:
            print(f"Не найдены утилиты: {', '.join(missing)}")
            if 'sshpass' in missing:
                print("  Установка: sudo apt-get install sshpass")
            sys.exit(1)

    def log(self, message):
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{ts}] {message}"
        print(line)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(line + '\n')

    # ── SSH ──────────────────────────────────────────────────────

    def _ssh(self, host, username, password, command, timeout=120):
        """Выполнение команды на сервере через SSH.
        Пароль передаётся через переменную окружения SSHPASS (sshpass -e)."""
        if self.dry_run:
            self.log(f"  [DRY RUN] SSH {username}@{host}: {command[:200]}")
            return "[DRY RUN]"

        env = os.environ.copy()
        cmd = [
            'ssh', '-o', 'StrictHostKeyChecking=no',
            '-o', 'ConnectTimeout=30',
            f'{username}@{host}', command
        ]
        if password:
            env['SSHPASS'] = password
            cmd = ['sshpass', '-e'] + cmd

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True,
                timeout=timeout, env=env
            )
            if result.returncode != 0:
                combined = (result.stdout + '\n' + result.stderr).strip()
                self.log(f"  SSH ошибка (код {result.returncode}): {combined[-2000:]}")
                raise subprocess.CalledProcessError(
                    result.returncode, cmd, result.stdout, result.stderr)
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            self.log(f"  Таймаут SSH ({timeout}с): {command[:100]}")
            raise

    def _ssh_docker(self, host, username, password, command, timeout=600):
        """Выполнение команды через ssh localhost -p<docker_port> (Docker Beget).
        Скрипт кодируется в base64 для надёжной передачи через вложенный SSH."""
        port = self.docker_port
        b64 = base64.b64encode(command.encode('utf-8')).decode('utf-8')
        wrapper = f'echo "{b64}" | base64 -d | ssh localhost -p{port} bash'
        return self._ssh(host, username, password, wrapper, timeout=timeout)

    # ── Шаги обновления ─────────────────────────────────────────

    def _step_git(self, host, username, password, site_path):
        """Инициализация git-репозитория и обновление до origin/<branch>.

        Файлы из .gitignore (local_settings.py, .env, venv/, migrations/,
        .htaccess, passenger_wsgi.py, media/) не затрагиваются."""
        self.log("── Git: инициализация и обновление ──")

        check = 'which git >/dev/null 2>&1 && echo "ok" || echo "no_git"'
        if 'no_git' in self._ssh(host, username, password, check):
            raise RuntimeError("git не установлен на сервере")

        init_cmd = (
            f'cd {site_path} && '
            f'git init 2>/dev/null && '
            f'(git remote add origin {self.git_repo} 2>/dev/null || '
            f' git remote set-url origin {self.git_repo}) && '
            f'git fetch origin {self.git_branch}'
        )
        self._ssh(host, username, password, init_cmd, timeout=180)

        checkout_cmd = (
            f'cd {site_path} && '
            f'git checkout -f -B {self.git_branch} origin/{self.git_branch}'
        )
        self._ssh(host, username, password, checkout_cmd)

        # Симлинк core → main/core (нужен для тем оформления)
        symlink_cmd = (
            f'cd {site_path} && '
            f'test -d main/core && {{ test -L core || ln -sf main/core core; }} || true'
        )
        self._ssh(host, username, password, symlink_cmd)

        log_cmd = f'cd {site_path} && git log --oneline -1'
        commit = self._ssh(host, username, password, log_cmd)
        self.log(f"  Коммит: {commit}")
        return commit

    def _step_deps(self, host, username, password, site_path):
        """Установка/обновление зависимостей через Docker-окружение.
        mysqlclient заменяется на PyMySQL (на Beget нет gcc для компиляции)."""
        self.log("── Установка зависимостей ──")

        check = f'test -f {site_path}/requirements.txt && echo "ok" || echo "missing"'
        if 'missing' in self._ssh(host, username, password, check):
            self.log("  requirements.txt не найден, пропуск")
            return

        check_venv = f'test -f {site_path}/venv/bin/activate && echo "ok" || echo "no_venv"'
        if 'no_venv' in self._ssh(host, username, password, check_venv):
            self.log("  venv не найден, пропуск (создайте вручную или через migrate.py)")
            return

        cmd = (
            f'source {site_path}/venv/bin/activate\n'
            f'cd {site_path}\n'
            f'cp requirements.txt /tmp/_req_update_$$.txt\n'
            f"sed -i 's/mysqlclient.*/PyMySQL>=1.0.0/' /tmp/_req_update_$$.txt\n"
            f'pip install -r /tmp/_req_update_$$.txt --quiet 2>&1 | tail -10\n'
            f'EXIT=$?\n'
            f'rm -f /tmp/_req_update_$$.txt\n'
            f'exit $EXIT\n'
        )
        try:
            out = self._ssh_docker(host, username, password, cmd)
            if out and out != "[DRY RUN]":
                self.log(f"  pip: {out[-500:]}")
            self.log("  Зависимости установлены")
        except Exception as e:
            self.log(f"  Предупреждение (deps): {e}")

    def _step_migrations(self, host, username, password, site_path):
        """makemigrations + migrate через Docker-окружение.
        Миграции не хранятся в git — генерируются на каждом сервере."""
        self.log("── Django миграции ──")

        manage = f"{site_path}/main"
        activate = f"source {site_path}/venv/bin/activate"

        mk_cmd = f'{activate}\ncd {manage}\npython manage.py makemigrations --no-input 2>&1\n'
        try:
            out = self._ssh_docker(host, username, password, mk_cmd)
            if out and out != "[DRY RUN]":
                self.log(f"  makemigrations: {out[-500:]}")
        except Exception as e:
            self.log(f"  Предупреждение (makemigrations): {e}")

        mig_cmd = f'{activate}\ncd {manage}\npython manage.py migrate --no-input 2>&1\n'
        out = self._ssh_docker(host, username, password, mig_cmd)
        if out and out != "[DRY RUN]":
            self.log(f"  migrate: {out[-500:]}")

    def _step_static(self, host, username, password, site_path):
        """collectstatic через Docker-окружение."""
        self.log("── Сбор статики ──")

        cmd = (
            f'source {site_path}/venv/bin/activate\n'
            f'cd {site_path}/main\n'
            f'python manage.py collectstatic --no-input 2>&1 | tail -5\n'
        )
        try:
            self._ssh_docker(host, username, password, cmd)
            self.log("  Статика собрана")
        except Exception as e:
            self.log(f"  Предупреждение (static): {e}")

    def _step_restart(self, host, username, password, site_path):
        """Перезапуск Passenger (touch tmp/restart.txt)."""
        self.log("── Перезапуск Passenger ──")

        cmd = (
            f'mkdir -p {site_path}/main/main/tmp && '
            f'touch {site_path}/main/main/tmp/restart.txt && echo "ok"'
        )
        res = self._ssh(host, username, password, cmd)
        if 'ok' in res:
            self.log("  Passenger перезапущен")
        else:
            self.log("  Предупреждение: не удалось перезапустить Passenger")

    def _step_verify_code(self, host, username, password, site_path):
        """Проверка: HEAD совпадает с origin/<branch>."""
        self.log("── Проверка актуальности кода ──")

        cmd = (
            f'cd {site_path} && '
            f'git fetch origin {self.git_branch} --quiet 2>/dev/null; '
            f'LOCAL=$(git rev-parse HEAD 2>/dev/null); '
            f'REMOTE=$(git rev-parse origin/{self.git_branch} 2>/dev/null); '
            f'if [ "$LOCAL" = "$REMOTE" ]; then echo "UP_TO_DATE"; '
            f'else echo "BEHIND local=$LOCAL remote=$REMOTE"; fi'
        )
        res = self._ssh(host, username, password, cmd)
        up_to_date = 'UP_TO_DATE' in res
        self.log(f"  Код: {'актуален' if up_to_date else res}")
        return up_to_date

    def _step_check_http(self, domain):
        """HTTP-проверка: сайт отвечает кодом 200."""
        self.log(f"── HTTP-проверка {domain} ──")

        if self.dry_run:
            self.log("  [DRY RUN] пропуск")
            return True

        time.sleep(3)

        for scheme in ('https', 'http'):
            url = f'{scheme}://{domain}'
            try:
                req = urllib.request.Request(
                    url, headers={'User-Agent': 'SiteUpdater/1.0'})
                ctx = ssl._create_unverified_context()
                resp = urllib.request.urlopen(req, timeout=30, context=ctx)
                code = resp.getcode()
                if code == 200:
                    self.log(f"  ✓ {url} → 200 OK")
                    return True
                self.log(f"  ✗ {url} → {code}")
            except Exception as e:
                self.log(f"  ✗ {url} → {e}")

        self.log(f"  Сайт {domain} НЕ отвечает!")
        return False

    # ── Оркестрация ──────────────────────────────────────────────

    def update_site(self, site_name):
        """Полный цикл обновления одного сайта."""
        if site_name not in self.config['sites']:
            self.log(f"Сайт '{site_name}' не найден в конфигурации")
            return False

        site = self.config['sites'][site_name]
        host = site['host']
        user = site['username']
        pwd = site.get('password', '')
        path = site['path']
        domain = site['domain']

        saved_port = self.docker_port
        self.docker_port = site.get('docker_port', self.docker_port)

        self.log(f"\n{'=' * 60}")
        self.log(f"Сайт: {site_name} ({domain})")
        self.log(f"Сервер: {user}@{host}:{path}")
        self.log(f"{'=' * 60}")

        r = {
            'domain': domain,
            'git': False, 'deps': False, 'migrations': False,
            'static': False, 'code_ok': False, 'http_ok': False,
            'commit': '', 'errors': []
        }

        try:
            r['commit'] = self._step_git(host, user, pwd, path)
            r['git'] = True
        except Exception as e:
            r['errors'].append(f"git: {e}")
            self.log(f"  ОШИБКА git: {e}")

        if r['git']:
            try:
                self._step_deps(host, user, pwd, path)
                r['deps'] = True
            except Exception as e:
                r['errors'].append(f"deps: {e}")
                self.log(f"  ОШИБКА deps: {e}")

            try:
                self._step_migrations(host, user, pwd, path)
                r['migrations'] = True
            except Exception as e:
                r['errors'].append(f"migrations: {e}")
                self.log(f"  ОШИБКА migrations: {e}")

            try:
                self._step_static(host, user, pwd, path)
                r['static'] = True
            except Exception as e:
                r['errors'].append(f"static: {e}")
                self.log(f"  ОШИБКА static: {e}")

            try:
                self._step_restart(host, user, pwd, path)
            except Exception as e:
                r['errors'].append(f"restart: {e}")

            try:
                r['code_ok'] = self._step_verify_code(host, user, pwd, path)
            except Exception as e:
                r['errors'].append(f"verify: {e}")

        try:
            r['http_ok'] = self._step_check_http(domain)
        except Exception as e:
            r['errors'].append(f"http: {e}")

        self.docker_port = saved_port
        self.results[site_name] = r
        return r['git'] and not r['errors']

    def update_all(self):
        """Обновление всех сайтов из конфигурации."""
        sites = list(self.config['sites'].keys())
        total = len(sites)
        self.log(f"Обновление {total} сайтов\n")

        for i, name in enumerate(sites, 1):
            self.log(f"[{i}/{total}]")
            try:
                self.update_site(name)
            except Exception as e:
                self.log(f"Критическая ошибка ({name}): {e}")

        self.print_summary()

    def check_only(self, site_name=None):
        """Только проверка без изменений: git-статус + HTTP."""
        sites = [site_name] if site_name else list(self.config['sites'].keys())

        for name in sites:
            site = self.config['sites'].get(name)
            if not site:
                self.log(f"Сайт '{name}' не найден")
                continue

            host = site['host']
            user = site['username']
            pwd = site.get('password', '')
            path = site['path']
            domain = site['domain']

            self.log(f"\n── Проверка: {name} ({domain}) ──")

            r = {
                'domain': domain,
                'git': False, 'deps': False, 'migrations': False,
                'static': False, 'code_ok': False, 'http_ok': False,
                'commit': '', 'errors': []
            }

            try:
                check = f'cd {path} && git rev-parse --short HEAD 2>/dev/null || echo "NO_GIT"'
                res = self._ssh(host, user, pwd, check)
                if 'NO_GIT' in res:
                    self.log("  Git не инициализирован")
                else:
                    r['commit'] = res
                    r['git'] = True
                    r['code_ok'] = self._step_verify_code(host, user, pwd, path)
            except Exception as e:
                r['errors'].append(str(e))

            try:
                r['http_ok'] = self._step_check_http(domain)
            except Exception as e:
                r['errors'].append(str(e))

            self.results[name] = r

        self.print_summary()

    def print_summary(self):
        """Итоговый отчёт по всем обработанным сайтам."""
        if not self.results:
            return

        self.log(f"\n{'=' * 60}")
        self.log("ИТОГОВЫЙ ОТЧЁТ")
        self.log(f"{'=' * 60}")

        ok_count = 0
        fail_count = 0

        for name, r in self.results.items():
            is_ok = (r.get('http_ok') and r.get('code_ok')
                     and not r.get('errors'))
            if is_ok:
                ok_count += 1
            else:
                fail_count += 1
            status = "✓ OK" if is_ok else "✗ ПРОБЛЕМА"

            self.log(f"\n  {name} ({r['domain']}): {status}")
            self.log(f"    Git:        {'✓' if r['git'] else '✗'}")
            self.log(f"    Зависимости:{'✓' if r['deps'] else '✗'}")
            self.log(f"    Миграции:   {'✓' if r['migrations'] else '✗'}")
            self.log(f"    Статика:    {'✓' if r['static'] else '✗'}")
            self.log(f"    Код:        {'✓ актуален' if r['code_ok'] else '✗ расходится'}")
            self.log(f"    HTTP:       {'✓ отвечает' if r['http_ok'] else '✗ не отвечает'}")
            if r.get('commit'):
                self.log(f"    Коммит:     {r['commit']}")
            for err in r.get('errors', []):
                self.log(f"    Ошибка:     {err}")

        self.log(f"\nИтого: {ok_count} OK, {fail_count} с проблемами")
        self.log(f"Лог: {self.log_file}")

    def list_sites(self):
        """Вывод списка сайтов из конфигурации."""
        sites = self.config.get('sites', {})
        print(f"Сайты в конфигурации ({len(sites)}):")
        for name, site in sites.items():
            print(f"  {name:30s}  {site.get('domain', '?'):30s}  {site.get('host', '?')}")


def main():
    parser = argparse.ArgumentParser(
        description='Обновление Django-сайтов на серверах Beget '
                    '(git pull + миграции + проверка)')
    parser.add_argument(
        '--config', '-c', default='update_config.json',
        help='Путь к конфигурации (default: update_config.json)')
    parser.add_argument(
        '--site', '-s',
        help='Обновить/проверить конкретный сайт (по имени из конфига)')
    parser.add_argument(
        '--list', '-l', action='store_true',
        help='Показать список сайтов из конфигурации')
    parser.add_argument(
        '--check', action='store_true',
        help='Только проверка (без изменений): git-статус + HTTP')
    parser.add_argument(
        '--dry-run', '-d', action='store_true',
        help='Тестовый запуск — команды выводятся, но не выполняются')

    args = parser.parse_args()
    updater = SiteUpdater(args.config, dry_run=args.dry_run)

    if args.dry_run:
        print(">>> РЕЖИМ DRY RUN — операции не выполняются <<<\n")

    if args.list:
        updater.list_sites()
    elif args.check:
        updater.check_only(args.site)
    elif args.site:
        updater.update_site(args.site)
        updater.print_summary()
    else:
        updater.update_all()


if __name__ == '__main__':
    main()

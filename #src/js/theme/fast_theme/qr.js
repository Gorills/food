$(document).ready(function() {
    $('.qr-products__cat').click(function(e) {
        $('.qr-products__cat').removeClass('qr-products__cat--active');
        $(this).addClass('qr-products__cat--active');
    });
});


$(document).ready(function() {
    $('.qr-header_call').click(function(e) {

        e.preventDefault();
        // Проверяем, не заблокирована ли кнопка
        if ($(this).hasClass('disabled')) {
            return;
        }

        var link = $(this).attr('href');
        $.get(link, function(data) {})

        // Сохраняем оригинальное содержимое
        let originalContent = $(this).html();
        
        // Добавляем класс блокировки
        $(this).addClass('disabled');
        
        // Заменяем содержимое на лоадер (простой пример)
        $(this).html(`<div class="loader">
                <?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                <svg width="15px" height="15px" style="margin-right:10px;" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M9.10745 2.67414C9.98414 2.24187 10.9649 2 12 2C15.7274 2 18.7491 5.13623 18.7491 9.00497V9.70957C18.7491 10.5552 18.9903 11.3818 19.4422 12.0854L20.5496 13.8095C21.5612 15.3843 20.789 17.5249 19.0296 18.0229C14.4273 19.3257 9.57274 19.3257 4.97036 18.0229C3.21105 17.5249 2.43882 15.3843 3.45036 13.8095L4.5578 12.0854C5.00972 11.3818 5.25087 10.5552 5.25087 9.70957V9.00497C5.25087 7.93058 5.48391 6.91269 5.90039 6.00277" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                <path d="M7.5 19C8.15503 20.7478 9.92246 22 12 22C12.2445 22 12.4847 21.9827 12.7192 21.9492M16.5 19C16.2329 19.7126 15.781 20.3428 15.1985 20.8393" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                </svg>

                Вызываем...
            
            </div>`);

        // Устанавливаем таймер на 5 секунд
        setTimeout(() => {
            // Возвращаем оригинальное содержимое
            $(this).html(originalContent);
            // Убираем класс блокировки
            $(this).removeClass('disabled');
        }, 3000);
    });
});


$(document).ready(function() {
    $('.cart-btn').click(function(e) {
       $('.qr-cart').addClass('qr-cart--active');
       $('body').addClass('body');
       $('.cart-btn').addClass('cart-btn--remove');
    });
});

$(document).ready(function() {
    $('.qr-cart__closer').click(function(e) {
       $('.qr-cart').removeClass('qr-cart--active');
       $('body').removeClass('body');
       $('.cart-btn').removeClass('cart-btn--remove');


    });
});



$(document).ready(function() {
    // Основной объект корзины
    const qr_cart = {
        // Инициализация корзины
        init: function() {
            this.loadCart();
            this.bindEvents();
        },

        // Загрузка корзины из localStorage
        loadCart: function() {
            const cartData = localStorage.getItem('qr_cart');
            this.items = cartData ? JSON.parse(cartData) : [];
            this.updateCartDisplay();
        },

        // Сохранение корзины в localStorage
        saveCart: function() {
            localStorage.setItem('qr_cart', JSON.stringify(this.items));
            this.updateCartDisplay();
        },

        // Модифицируем addItem
        addItem: function(itemId, name, price, modifiers = [], image = '') {
            const existingItem = this.items.find(item => 
                item.id === itemId && 
                JSON.stringify(item.modifiers) === JSON.stringify(modifiers)
            );

            if (existingItem) {
                existingItem.quantity++;
            } else {
                this.items.push({
                    id: itemId,
                    name: name,
                    price: parseFloat(price),
                    quantity: 1,
                    modifiers: modifiers,
                    image: image // Добавляем поле для изображения
                });
            }
            this.saveCart();
        },

        // Удаление товара из корзины
        removeItem: function(itemId, modifiers = []) {
            this.items = this.items.filter(item => 
                !(item.id === itemId && 
                JSON.stringify(item.modifiers) === JSON.stringify(modifiers))
            );
            this.saveCart();
        },

        // Изменение количества товара
        updateQuantity: function(itemId, modifiers, quantity) {
            const item = this.items.find(item => 
                item.id === itemId && 
                JSON.stringify(item.modifiers) === JSON.stringify(modifiers)
            );
            if (item) {
                quantity = parseInt(quantity);
                if (quantity <= 0) {
                    this.removeItem(itemId, modifiers);
                } else {
                    item.quantity = quantity;
                    this.saveCart();
                }
            }
        },

        // Добавление модификатора к существующему товару
        addModifier: function(itemId, modifier) {
            const item = this.items.find(item => item.id === itemId);
            if (item && !item.modifiers.some(m => m.id === modifier.id)) {
                item.modifiers.push(modifier);
                this.saveCart();
            }
        },

        // Удаление модификатора из товара
        removeModifier: function(itemId, modifierId) {
            const item = this.items.find(item => item.id === itemId);
            if (item) {
                item.modifiers = item.modifiers.filter(m => m.id !== modifierId);
                this.saveCart();
            }
        },

        // Получение общей суммы
        getTotal: function() {
            return this.items.reduce((total, item) => {
                const modifiersTotal = item.modifiers.reduce((sum, mod) => sum + (mod.price || 0), 0);
                return total + (item.price + modifiersTotal) * item.quantity;
            }, 0).toFixed(2);
        },

        // Очистка корзины
        clearCart: function() {
            this.items = [];
            this.saveCart();
        },

        // Обновление отображения корзины
        updateCartDisplay: function() {
            const $cartContainer = $('#cart-items');
            $cartContainer.empty();

            if (this.items.length === 0) {
                $cartContainer.html('<p class="cart__empty-text">Корзина пуста</p>');
            } else {
                this.items.forEach((item, index) => {
                    const modifiersHtml = item.modifiers.map(mod => `
                        <div class="cart-modifier">
                            ${mod.name} (+${mod.price}₽)
                        </div>
                    `).join('');

                    const itemHtml = `
                        <div class="cart-item" data-item-id="${item.id}" data-modifiers='${JSON.stringify(item.modifiers)}'>
                            <div class="cart-item__image">
                                <img src="${item.image || '/core/libs/no-image.webp'}" alt="${item.name}" class="cart-thumb">
                                
                            </div>
                            
                            <div class="cart-item__right">
                                <h4>${item.name} - ${item.price}₽</h4>
                                <div class="cart-item__modifiers">
                                ${modifiersHtml}
                                </div>

                                <div class="qr-cart__wrapper">
                                    <div class="quantity-control">
                                        <button class="decrease-qty">-</button>
                                        <input type="number" value="${item.quantity}" min="1" class="quantity">
                                        <button class="increase-qty">+</button>
                                    </div>
                                    <button class="remove-item">
                                        <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M20.5001 6H3.5" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"></path>
                                        <path d="M9.5 11L10 16" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"></path>
                                        <path d="M14.5 11L14 16" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"></path>
                                        <path d="M6.5 6C6.55588 6 6.58382 6 6.60915 5.99936C7.43259 5.97849 8.15902 5.45491 8.43922 4.68032C8.44784 4.65649 8.45667 4.62999 8.47434 4.57697L8.57143 4.28571C8.65431 4.03708 8.69575 3.91276 8.75071 3.8072C8.97001 3.38607 9.37574 3.09364 9.84461 3.01877C9.96213 3 10.0932 3 10.3553 3H13.6447C13.9068 3 14.0379 3 14.1554 3.01877C14.6243 3.09364 15.03 3.38607 15.2493 3.8072C15.3043 3.91276 15.3457 4.03708 15.4286 4.28571L15.5257 4.57697C15.5433 4.62992 15.5522 4.65651 15.5608 4.68032C15.841 5.45491 16.5674 5.97849 17.3909 5.99936C17.4162 6 17.4441 6 17.5 6" stroke="#1C274C" stroke-width="1.5"></path>
                                        <path d="M18.3735 15.3991C18.1965 18.054 18.108 19.3815 17.243 20.1907C16.378 21 15.0476 21 12.3868 21H11.6134C8.9526 21 7.6222 21 6.75719 20.1907C5.89218 19.3815 5.80368 18.054 5.62669 15.3991L5.16675 8.5M18.8334 8.5L18.6334 11.5" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"></path>
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    `;
                    $cartContainer.append(itemHtml);
                });
            }
            $('#cart-total').text(`Итого: ${this.getTotal()}₽`);
            $('#cart-total-btn').text(`Заказ / ${this.getTotal()} ₽`);

            
        },

        // Отправка корзины на сервер
        sendCartToServer: function(tableId) {
            const cartData = this.items; // Получаем текущие элементы корзины
            if (cartData.length === 0) {
                alert('Корзина пуста!');
                return;
            }

            $.ajax({
                url: '/qr_menu/order/'+tableId+'/', // URL endpoint
                type: 'POST',
                data: JSON.stringify(cartData), // Преобразуем корзину в JSON
                contentType: 'application/json', // Указываем тип данных
                success: function(response) {
                    console.log('Корзина успешно отправлена:', response);
                    // Можно добавить очистку корзины после успешной отправки
                    qr_cart.clearCart();
                    alert('Заказ успешно оформлен!');
                    // Перенаправление, если нужно
                    window.location.href = '/qr_menu/order/success/'+tableId+'/'; // Пример
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при отправке корзины:', error);
                    alert('Произошла ошибка при оформлении заказа.');
                }
            });
        },

        // Привязка событий
        bindEvents: function() {
            const self = this;

            // Увеличение количества
            $(document).on('click', '.increase-qty', function() {
                const $item = $(this).closest('.cart-item');
                const itemId = $item.data('item-id');
                const modifiers = JSON.parse($item.attr('data-modifiers'));
                const $quantity = $item.find('.quantity');
                self.updateQuantity(itemId, modifiers, parseInt($quantity.val()) + 1);
            });

            // Уменьшение количества
            $(document).on('click', '.decrease-qty', function() {
                const $item = $(this).closest('.cart-item');
                const itemId = $item.data('item-id');
                const modifiers = JSON.parse($item.attr('data-modifiers'));
                const $quantity = $item.find('.quantity');
                self.updateQuantity(itemId, modifiers, parseInt($quantity.val()) - 1);
            });

            // Ручной ввод количества
            $(document).on('change', '.quantity', function() {
                const $item = $(this).closest('.cart-item');
                const itemId = $item.data('item-id');
                const modifiers = JSON.parse($item.attr('data-modifiers'));
                self.updateQuantity(itemId, modifiers, $(this).val());
            });

            // Удаление товара
            $(document).on('click', '.remove-item', function() {
                const $item = $(this).closest('.cart-item');
                const itemId = $item.data('item-id');
                const modifiers = JSON.parse($item.attr('data-modifiers'));
                self.removeItem(itemId, modifiers);
            });

            // Удаление модификатора
            $(document).on('click', '.remove-modifier', function() {
                const itemId = $(this).data('item-id');
                const modifierId = $(this).data('modifier-id');
                self.removeModifier(itemId, modifierId);
            });

            // Очистка корзины
            $(document).on('click', '#clear-cart', function() {
                self.clearCart();
            });

            // Обработчик для кнопки "Оформить заказ"
            $(document).on('click', '.qr-header_call', function(e) {
                e.preventDefault(); // Предотвращаем переход по ссылке
                const tableId = $(this).data('table-id');
                self.sendCartToServer(tableId); // Отправляем корзину
            });
        }
    };



    let currentProduct = null;

    // Обработчик клика для кнопки добавления
    $(document).on('click', '.qr-products__btn', function(e) {
        e.preventDefault();

        const productId = $(this).data('product-id');
        const productName = $(this).data('product-name');
        const productPrice = $(this).data('product-price');
        const productImage = $(this).data('product-image'); // Получаем URL изображения
        let options = $(this).data('options');

        try {
            options = typeof options === 'string' && options ? JSON.parse(options) : options;
        } catch (e) {
            console.error('Error parsing options:', e);
            options = [];
        }

        currentProduct = { id: productId, name: productName, price: productPrice, image: productImage };

        if (!options || options.length === 0) {
            qr_cart.addItem(productId, productName, productPrice, [], productImage); // Передаем изображение
            showFeedback($(this));
        } else {
            showOptionsModal(options);
        }
    });

    // Показать модальное окно с опциями
    function showOptionsModal(optionTypes) {
        const $modifiersList = $('#modifiers-list');
        $modifiersList.empty();

        $.each(optionTypes, function(index, optionType) {
            const optionClass = optionType.option_class;
            const isRadio = optionClass === 'radio' || optionClass === 'select'; // select обрабатываем как radio
            let html = `<div class="option-group"><h4>${optionType.name}</h4>`;

            $.each(optionType.options, function(i, option) {
                html += `
                    <label>
                        <input 
                            type="${isRadio ? 'radio' : 'checkbox'}" 
                            class="modifier" 
                            name="${isRadio ? 'option_' + optionType.id : option.id}" 
                            data-id="${option.id}" 
                            data-name="${option.option_value}" 
                            data-price="${option.option_price}"
                            ${isRadio && i === 0 ? 'checked' : ''}>
                        ${option.option_value} ${option.option_price ? '(+' + option.option_price + '₽)' : ''}
                    </label>
                `;
            });

            html += '</div>';
            $modifiersList.append(html);
        });

        $('#modifiers-modal').show();
    }

    // Подтверждение выбора опций
    $('#confirm-modifiers').click(function() {
        if (!currentProduct) return;

        const selectedOptions = $('.modifier:checked').map(function() {
            return {
                id: $(this).data('id'),
                name: $(this).data('name'),
                price: parseFloat($(this).data('price') || 0)
            };
        }).get();

        qr_cart.addItem(
            currentProduct.id,
            currentProduct.name,
            currentProduct.price,
            selectedOptions,
            currentProduct.image // Передаем изображение
        );

        $('#modifiers-modal').hide();
        showFeedback($(`.qr-products__btn[data-product-id="${currentProduct.id}"]`));
        currentProduct = null;
    });

    // Закрытие модального окна
    $('#close-modal').click(function() {
        $('#modifiers-modal').hide();
        currentProduct = null;
    });

    // Визуальная обратная связь
    function showFeedback($button) {
        $button.text('✓').addClass('added');
        setTimeout(() => {
            $button.text('+').removeClass('added');
        }, 1000);
    }

    // Инициализация корзины
    qr_cart.init();
    window.qr_cart = qr_cart;
});



"use strict";

import { paths } from "../gulpfile.babel";
import gulp from "gulp";
import browsersync from "browser-sync";

gulp.task("serve", () => {
    browsersync.init({
		notify: false,
        port: 3000,
        proxy: 'localhost:8000'
	});

    gulp.watch(paths.views.watch, gulp.parallel("views"));
    gulp.watch(paths.global_views.watch, gulp.parallel("global_views"));
    gulp.watch(paths.global_js.watch, gulp.parallel("global_js"));
    gulp.watch(paths.styles.watch, gulp.parallel("styles"));
    gulp.watch(paths.scripts.watch, gulp.parallel("scripts"));
    gulp.watch(paths.sprites.watch, gulp.parallel("sprites"));
    gulp.watch(paths.images.watch, gulp.parallel("images"));
    gulp.watch(paths.fonts.watch, gulp.parallel("fonts"));

    gulp.watch(paths.chinaviews.watch, gulp.parallel("chinaviews"));
    gulp.watch(paths.global_chinaviews.watch, gulp.parallel("global_chinaviews"));
    gulp.watch(paths.global_chinajs.watch, gulp.parallel("global_chinajs"));
    gulp.watch(paths.chinastyles.watch, gulp.parallel("chinastyles"));
    gulp.watch(paths.chinascripts.watch, gulp.parallel("chinascripts"));
    gulp.watch(paths.chinasprites.watch, gulp.parallel("chinasprites"));
    gulp.watch(paths.chinaimages.watch, gulp.parallel("chinaimages"));
    gulp.watch(paths.chinafonts.watch, gulp.parallel("chinafonts"));

    gulp.watch(paths.sushi_views.watch, gulp.parallel("sushi_views"));
    gulp.watch(paths.global_sushi_views.watch, gulp.parallel("global_sushi_views"));
    gulp.watch(paths.sushi_js.watch, gulp.parallel("sushi_js"));
    gulp.watch(paths.sushi_styles.watch, gulp.parallel("sushi_styles"));
    gulp.watch(paths.sushi_change_fonts.watch, gulp.parallel("sushi_change_fonts"));
    gulp.watch(paths.sushi_scripts.watch, gulp.parallel("sushi_scripts"));
    gulp.watch(paths.sushi_sprites.watch, gulp.parallel("sushi_sprites"));
    gulp.watch(paths.sushi_images.watch, gulp.parallel("sushi_images"));
    gulp.watch(paths.sushi_fonts.watch, gulp.parallel("sushi_fonts"));
    

    gulp.watch(paths.adminviews.watch, gulp.parallel("adminviews"));
    gulp.watch(paths.adminstyles.watch, gulp.parallel("adminstyles"));
    gulp.watch(paths.adminscripts.watch, gulp.parallel("adminscripts"));
    gulp.watch(paths.adminsprites.watch, gulp.parallel("adminsprites"));
    gulp.watch(paths.adminimages.watch, gulp.parallel("adminimages"));
    gulp.watch(paths.adminfonts.watch, gulp.parallel("adminfonts"));
});
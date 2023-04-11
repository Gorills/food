"use strict";

import { paths } from "../gulpfile.babel";
import gulp from "gulp";
import debug from "gulp-debug";

gulp.task("fonts", () => {
    return gulp.src(paths.fonts.src)
        .pipe(gulp.dest(paths.fonts.dist))
        .pipe(debug({
            "title": "Fonts"
        }));
});

gulp.task("chinafonts", () => {
    return gulp.src(paths.chinafonts.src)
        .pipe(gulp.dest(paths.chinafonts.dist))
        .pipe(debug({
            "title": "Fonts"
        }));
});

gulp.task("sushi_fonts", () => {
    return gulp.src(paths.sushi_fonts.src)
        .pipe(gulp.dest(paths.sushi_fonts.dist))
        .pipe(debug({
            "title": "Fonts"
        }));
});

gulp.task("adminfonts", () => {
    return gulp.src(paths.adminfonts.src)
        .pipe(gulp.dest(paths.adminfonts.dist))
        .pipe(debug({
            "title": "Fonts"
        }));
});
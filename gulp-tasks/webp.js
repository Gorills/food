"use strict";

import { paths } from "../gulpfile.babel";
import gulp from "gulp";
import gulpif from "gulp-if";
import imageminWebp from "imagemin-webp";
import webp from "gulp-webp";
import newer from "gulp-newer";
import debug from "gulp-debug";
import browsersync from "browser-sync";
import yargs from "yargs";

const argv = yargs.argv,
    production = !!argv.production;

gulp.task("webp", () => {
    return gulp.src(paths.images.src)
        .pipe(newer(paths.images.dist))
        .pipe(webp(gulpif(production, imageminWebp({
            lossless: true,
            quality: 100,
            alphaQuality: 100
        }))))
        .pipe(gulp.dest(paths.images.dist))
        .pipe(debug({
            "title": "Images"
        }))
        .on("end", browsersync.reload);
});

gulp.task("chinawebp", () => {
    return gulp.src(paths.chinaimages.src)
        .pipe(newer(paths.chinaimages.dist))
        .pipe(webp(gulpif(production, imageminWebp({
            lossless: true,
            quality: 100,
            alphaQuality: 100
        }))))
        .pipe(gulp.dest(paths.chinaimages.dist))
        .pipe(debug({
            "title": "Images"
        }))
        .on("end", browsersync.reload);
});
gulp.task("sushi_webp", () => {
    return gulp.src(paths.sushi_images.src)
        .pipe(newer(paths.sushi_images.dist))
        .pipe(webp(gulpif(production, imageminWebp({
            lossless: true,
            quality: 100,
            alphaQuality: 100
        }))))
        .pipe(gulp.dest(paths.sushi_images.dist))
        .pipe(debug({
            "title": "Images"
        }))
        .on("end", browsersync.reload);
});

gulp.task("fast_webp", () => {
    return gulp.src(paths.sushi_images.src)
        .pipe(newer(paths.sushi_images.dist))
        .pipe(webp(gulpif(production, imageminWebp({
            lossless: true,
            quality: 100,
            alphaQuality: 100
        }))))
        .pipe(gulp.dest(paths.sushi_images.dist))
        .pipe(debug({
            "title": "Images"
        }))
        .on("end", browsersync.reload);
});


gulp.task("flowers_light_webp", () => {
    return gulp.src(paths.sushi_images.src)
        .pipe(newer(paths.sushi_images.dist))
        .pipe(webp(gulpif(production, imageminWebp({
            lossless: true,
            quality: 100,
            alphaQuality: 100
        }))))
        .pipe(gulp.dest(paths.sushi_images.dist))
        .pipe(debug({
            "title": "Images"
        }))
        .on("end", browsersync.reload);
});



gulp.task("adminwebp", () => {
    return gulp.src(paths.adminimages.src)
        .pipe(newer(paths.adminimages.dist))
        .pipe(webp(gulpif(production, imageminWebp({
            lossless: true,
            quality: 100,
            alphaQuality: 100
        }))))
        .pipe(gulp.dest(paths.adminimages.dist))
        .pipe(debug({
            "title": "Images"
        }))
        .on("end", browsersync.reload);
});

"use strict";

import { paths } from "../gulpfile.babel";
import webpack from "webpack";
import webpackStream from "webpack-stream";
import gulp from "gulp";
import gulpif from "gulp-if";
import rename from "gulp-rename";
import browsersync from "browser-sync";
import debug from "gulp-debug";
import yargs from "yargs";

const webpackConfig = require("../webpack.config.js"),
    argv = yargs.argv,
    production = !!argv.production;

webpackConfig.mode = production ? "production" : "development";
webpackConfig.devtool = production ? false : "source-map";

gulp.task("scripts", () => {
    return gulp.src(paths.scripts.src)
    
		.pipe(gulp.dest(paths.scripts.dist))

		.pipe(gulp.dest(paths.scripts.dist))
		.pipe(browsersync.stream());
});

gulp.task("global_js", () => {
    return gulp.src(paths.global_js.src)
    
		.pipe(gulp.dest(paths.global_js.dist))

		.pipe(gulp.dest(paths.global_js.dist))
		.pipe(browsersync.stream());
});

gulp.task("global_chinajs", () => {
    return gulp.src(paths.global_chinajs.src)
    
		.pipe(gulp.dest(paths.global_chinajs.dist))

		.pipe(gulp.dest(paths.global_chinajs.dist))
		.pipe(browsersync.stream());
});

gulp.task("chinascripts", () => {
    return gulp.src(paths.chinascripts.src)
		.pipe(gulp.dest(paths.chinascripts.dist))

		.pipe(gulp.dest(paths.chinascripts.dist))
		.pipe(browsersync.stream());
});

gulp.task("adminscripts", () => {
    return gulp.src(paths.adminscripts.src)
    .pipe(gulp.dest(paths.adminscripts.dist))

    .pipe(gulp.dest(paths.adminscripts.dist))
    .pipe(browsersync.stream());
});
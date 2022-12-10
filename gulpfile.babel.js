"use strict";

import gulp from "gulp";

const requireDir = require("require-dir"),
    paths = {
        views: {
            src: [
                "./#src/templates/theme/default/**/*.html",
                "./#src/templates/theme/default/pages/*.html"
            ],
            dist: "./main/core/theme/default/views/",
            watch: [
                "./#src/templates/theme/default/**/*.html",
                "./#src/templates/theme/default/pages/*.html"
            ]
        },
        global_views: {
            src: [
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ],
            dist: "./main/core/theme/default/views/global/",
            watch: [
                "./#src/templates/global/default/**/*.html",
                "./#src/templates/global/default/pages/*.html"
            ]
        },
        styles: {
            src: "./#src/scss/theme/default/style.{scss,sass}",
            dist: "./main/core/theme/default/css/",
            watch: [
                "./#src/scss/theme/default/**/*.{scss,sass}",
                "./#src/scss/theme/default/**/*.{scss,sass}"
            ]
        },
        scripts: {
            src: "./#src/js/theme/default/app.js",
            dist: "./main/core/theme/default/js/",
            watch: [
                "./#src/js/theme/default/**/*.js",
                "./#src/js/theme/default/**/*.js",
              
            ]
        },
        images: {
            src: [
                "./#src/images/theme/default/**/*.{jpg,jpeg,png,gif,tiff,svg}",
                "!./#src/images/theme/default/fav/*.{jpg,jpeg,png,gif,tiff}"
            ],
            dist: "./main/core/theme/default/images/",
            watch: "./#src/images/theme/default/**/*.{jpg,jpeg,png,gif,svg,tiff}"
        },
        sprites: {
            src: "./#src/images/theme/default/sprites/*.svg",
            dist: "./main/core/theme/default/images/sprites/",
            watch: "./#src/images/theme/default/sprites/*.svg"
        },
        fonts: {
            src: "./#src/fonts/theme/default/**/*.{woff,woff2,ttf}",
            dist: "./main/core/theme/default/fonts/",
            watch: "./#src/fonts/theme/default/**/*.{woff,woff2,ttf}"
        },
        favicons: {
            src: "./#src/img/theme/default/fav/*.{jpg,jpeg,png,gif}",
            dist: "./main/core/img/fav/",
        },
        // gzip: {
        //     src: "./#src/.htaccess",
        //     dist: "./main/core/"
        // },
        // theme china
        chinaviews: {
            src: [
                "./#src/templates/theme/china/**/*.html",
                "./#src/templates/theme/china/pages/*.html"
            ],
            dist: "./main/core/theme/china/views/",
            watch: [
                "./#src/templates/theme/china/**/*.html",
                "./#src/templates/theme/china/pages/*.html"
            ]
        },
        global_chinaviews: {
            src: [
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ],
            dist: "./main/core/theme/china/views/global/",
            watch: [
                "./#src/templates/global/default/**/*.html",
                "./#src/templates/global/default/pages/*.html"
            ]
        },
        chinastyles: {
            src: "./#src/scss/theme/china/style.{scss,sass}",
            dist: "./main/core/theme/china/css/",
            watch: [
                "./#src/scss/theme/china/**/*.{scss,sass}",
                "./#src/scss/theme/china/**/*.{scss,sass}"
            ]
        },
        chinascripts: {
            src: "./#src/js/theme/china/app.js",
            dist: "./main/core/theme/china/js/",
            watch: [
                "./#src/js/theme/china/**/*.js",
                "./#src/js/theme/china/**/*.js"
            ]
        },
        chinaimages: {
            src: [
                "./#src/images/theme/china/**/*.{jpg,jpeg,png,gif,tiff,svg}",
                "!./#src/images/theme/china/fav/*.{jpg,jpeg,png,gif,tiff}"
            ],
            dist: "./main/core/theme/china/images/",
            watch: "./#src/images/theme/china/**/*.{jpg,jpeg,png,gif,svg,tiff}"
        },
        chinasprites: {
            src: "./#src/images/theme/china/sprites/*.svg",
            dist: "./main/core/theme/china/images/sprites/",
            watch: "./#src/images/theme/china/sprites/*.svg"
        },
        chinafonts: {
            src: "./#src/fonts/theme/china/**/*.{woff,woff2,ttf}",
            dist: "./main/core/theme/china/fonts/",
            watch: "./#src/fonts/theme/china/**/*.{woff,woff2,ttf}"
        },
        chinafavicons: {
            src: "./#src/img/theme/china/fav/*.{jpg,jpeg,png,gif}",
            dist: "./main/core/img/fav/",
        },
        chinagzip: {
            src: "./#src/.htaccess",
            dist: "./main/core/"
        },
        // admin
        adminviews: {
            src: [
                "./#src/templates/admin/**/*.html",
                "./#src/templates/admin/pages/*.html"
            ],
            dist: "./main/core/admin/views/",
            watch: [
                "./#src/templates/admin/**/*.html",
                "./#src/templates/admin/pages/*.html"
            ]
        },
        adminstyles: {
            src: "./#src/scss/admin/style.{scss,sass}",
            dist: "./main/core/admin/css/",
            watch: [
                "./#src/scss/admin/**/*.{scss,sass}",
                "./#src/scss/admin/**/*.{scss,sass}"
            ]
        },
        adminscripts: {
            src: "./#src/js/admin/app.js",
            dist: "./main/core/admin/js/",
            watch: [
                "./#src/js/admin/**/*.js",
                "./#src/js/admin/**/*.js"
            ]
        },
        adminimages: {
            src: [
                "./#src/images/admin/**/*.{jpg,jpeg,png,gif,tiff,svg}",
                "!./#src/images/admin/fav/*.{jpg,jpeg,png,gif,tiff}"
            ],
            dist: "./main/core/admin/images/",
            watch: "./#src/images/admin/**/*.{jpg,jpeg,png,gif,svg,tiff}"
        },
        adminsprites: {
            src: "./#src/images/admin/sprites/*.svg",
            dist: "./main/core/admin/images/sprites/",
            watch: "./#src/images/admin/sprites/*.svg"
        },
        adminfonts: {
            src: "./#src/fonts/admin/**/*.{woff,woff2,ttf}",
            dist: "./main/core/admin/fonts/",
            watch: "./#src/fonts/admin/**/*.{woff,woff2,ttf}"
        },
        adminfavicons: {
            src: "./#src/img/admin/fav/*.{jpg,jpeg,png,gif}",
            dist: "./main/core/img/fav/",
        }
    };

requireDir("./gulp-tasks/");

export { paths };

export const development = gulp.series("clean", "adminclean",
    gulp.parallel([
        "views", 
        'global_views',
        "styles", 
        "scripts", 
        "images", 
        "webp", 
        "sprites", 
        "fonts", 
        "favicons",
        "chinaviews", 
        'global_chinaviews',
        "chinastyles", 
        "chinascripts", 
        "chinaimages", 
        "chinawebp", 
        "chinasprites", 
        "chinafonts", 
        "chinafavicons",
        "adminviews", 
        "adminstyles", 
        "adminscripts", 
        "adminimages", 
        "adminwebp", 
        "adminsprites", 
        "adminfonts", 
        "adminfavicons"
    
    ]),
    gulp.parallel("serve"));

export const prod = gulp.series("clean", "adminclean",
    gulp.parallel([
        "views", 
        "styles", 
        "scripts", 
        "images", 
        "webp", 
        "sprites", 
        "fonts", 
        "favicons", 
        // "gzip",
        "chinaviews", 
        'global_chinaviews',
        "chinastyles", 
        "chinascripts", 
        "chinaimages", 
        "chinawebp", 
        "chinasprites", 
        "chinafonts", 
        "chinafavicons", 
        // "chinagzip",
        "adminviews", 
        "adminstyles", 
        "adminscripts", 
        "adminimages", 
        "adminwebp", 
        "adminsprites", 
        "adminfonts", 
        "adminfavicons",
    ]));

export default development;
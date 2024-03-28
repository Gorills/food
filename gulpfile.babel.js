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
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ]
        },
        global_js: {
            src: [
                "./#src/js/theme/global/**/*.js",
                
            ],
            dist: "./main/core/theme/default/js/",
            watch: [
                "./#src/js/theme/global/**/*.js",
            ]
        },
        styles: {
            src: "./#src/scss/theme/default/style.{scss,sass}",
            dist: "./main/core/theme/default/css/",
            watch: [
                "./#src/scss/theme/default/**/*.{scss,sass}",
                "./#src/scss/theme/default/**/*.{scss,sass}",
                "./#src/scss/theme/global/**/*.{scss,sass}"

                
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
                "./#src/images/theme/default/**/*.{jpg,jpeg,png,gif,tiff,svg,webp}",
                "!./#src/images/theme/default/fav/*.{jpg,jpeg,png,gif,tiff,webp}"
            ],
            dist: "./main/core/theme/default/images/",
            watch: "./#src/images/theme/default/**/*.{jpg,jpeg,png,gif,svg,tiff,webp}"
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


        // Тема sushi
        sushi_views: {
            src: [
                "./#src/templates/theme/sushi/**/*.html",
                "./#src/templates/theme/sushi/pages/*.html"
            ],
            dist: "./main/core/theme/sushi/views/",
            watch: [
                "./#src/templates/theme/sushi/**/*.html",
                "./#src/templates/theme/sushi/pages/*.html"
            ]
        },
        global_sushi_views: {
            src: [
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ],
            dist: "./main/core/theme/sushi/views/global/",
            watch: [
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ]
        },
        sushi_js: {
            src: [
                "./#src/js/theme/global/**/*.js",
                
            ],
            dist: "./main/core/theme/sushi/js/",
            watch: [
                "./#src/js/theme/global/**/*.js",
            ]
        },
        sushi_styles: {
            src: "./#src/scss/theme/sushi/style.{scss,sass}",
            dist: "./main/core/theme/sushi/css/",
            watch: [
                "./#src/scss/theme/sushi/**/*.{scss,sass}",
                "./#src/scss/theme/sushi/**/*.{scss,sass}",
                "./#src/scss/theme/global/**/*.{scss,sass}"

                
            ]
        },
        sushi_change_fonts: {
            src: "./#src/scss/theme/sushi/fonts/**/*.{scss,sass}",
            dist: "./main/core/theme/sushi/css/fonts/",
            watch: [
                "./#src/scss/theme/sushi/fonts/**/*.{scss,sass}",
                "./#src/scss/theme/sushi/fonts/**/*.{scss,sass}",
                "./#src/scss/theme/sushi/fonts/**/*.{scss,sass}"

                
            ]
        },
        sushi_scripts: {
            src: "./#src/js/theme/sushi/app.js",
            dist: "./main/core/theme/sushi/js/",
            watch: [
                "./#src/js/theme/sushi/**/*.js",
                "./#src/js/theme/sushi/**/*.js",
              
            ]
        },
        sushi_images: {
            src: [
                "./#src/images/theme/sushi/**/*.{jpg,jpeg,png,gif,tiff,svg,webp}",
                "!./#src/images/theme/sushi/fav/*.{jpg,jpeg,png,gif,tiff,webp}"
            ],
            dist: "./main/core/theme/sushi/images/",
            watch: "./#src/images/theme/sushi/**/*.{jpg,jpeg,png,gif,svg,tiff,webp}"
        },
        sushi_sprites: {
            src: "./#src/images/theme/sushi/sprites/*.svg",
            dist: "./main/core/theme/sushi/images/sprites/",
            watch: "./#src/images/theme/sushi/sprites/*.svg"
        },
        sushi_fonts: {
            src: "./#src/fonts/theme/sushi/**/*.{woff,woff2,ttf,TTF,otf}",
            dist: "./main/core/theme/sushi/fonts/",
            watch: "./#src/fonts/theme/sushi/**/*.{woff,woff2,ttf,TTF,otf}"
        },
        sushi_favicons: {
            src: "./#src/img/theme/sushi/fav/*.{jpg,jpeg,png,gif}",
            dist: "./main/core/img/fav/",
        },

        // Тема fast
        fast_views: {
            src: [
                "./#src/templates/theme/fast_theme/**/*.html",
                "./#src/templates/theme/fast_theme/pages/*.html"
            ],
            dist: "./main/core/theme/fast_theme/views/",
            watch: [
                "./#src/templates/theme/fast_theme/**/*.html",
                "./#src/templates/theme/fast_theme/pages/*.html"
            ]
        },
        global_fast_views: {
            src: [
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ],
            dist: "./main/core/theme/fast_theme/views/global/",
            watch: [
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ]
        },
        fast_js: {
            src: [
                "./#src/js/theme/global/**/*.js",
                
            ],
            dist: "./main/core/theme/fast_theme/js/",
            watch: [
                "./#src/js/theme/global/**/*.js",
            ]
        },
        fast_styles: {
            src: "./#src/scss/theme/fast_theme/style.{scss,sass}",
            dist: "./main/core/theme/fast_theme/css/",
            watch: [
                "./#src/scss/theme/fast_theme/**/*.{scss,sass}",
                "./#src/scss/theme/fast_theme/**/*.{scss,sass}",
                "./#src/scss/theme/global/**/*.{scss,sass}"

                
            ]
        },
        fast_change_fonts: {
            src: "./#src/scss/theme/fast_theme/fonts/**/*.{scss,sass}",
            dist: "./main/core/theme/fast_theme/css/fonts/",
            watch: [
                "./#src/scss/theme/fast_theme/fonts/**/*.{scss,sass}",
                "./#src/scss/theme/fast_theme/fonts/**/*.{scss,sass}",
                "./#src/scss/theme/fast_theme/fonts/**/*.{scss,sass}"

                
            ]
        },
        fast_scripts: {
            src: "./#src/js/theme/fast_theme/*.js",
            dist: "./main/core/theme/fast_theme/js/",
            watch: [
                "./#src/js/theme/fast_theme/**/*.js",
                "./#src/js/theme/fast_theme/**/*.js",
              
            ]
        },
        fast_images: {
            src: [
                "./#src/images/theme/fast_theme/**/*.{jpg,jpeg,png,gif,tiff,svg,webp}",
                "!./#src/images/theme/fast_theme/fav/*.{jpg,jpeg,png,gif,tiff,webp}"
            ],
            dist: "./main/core/theme/fast_theme/images/",
            watch: "./#src/images/theme/fast_theme/**/*.{jpg,jpeg,png,gif,svg,tiff,webp}"
        },
        fast_sprites: {
            src: "./#src/images/theme/fast_theme/sprites/*.svg",
            dist: "./main/core/theme/fast_theme/images/sprites/",
            watch: "./#src/images/theme/fast_theme/sprites/*.svg"
        },
        fast_fonts: {
            src: "./#src/fonts/theme/fast_theme/**/*.{woff,woff2,ttf,TTF,otf}",
            dist: "./main/core/theme/fast_theme/fonts/",
            watch: "./#src/fonts/theme/fast_theme/**/*.{woff,woff2,ttf,TTF,otf}"
        },
        fast_favicons: {
            src: "./#src/img/theme/fast_theme/fav/*.{jpg,jpeg,png,gif}",
            dist: "./main/core/img/fav/",
        },

        // Цветы светлая

        
        flowers_light_views: {
            src: [
                "./#src/templates/theme/flowers_light/**/*.html",
                "./#src/templates/theme/flowers_light/pages/*.html"
            ],
            dist: "./main/core/theme/flowers_light/views/",
            watch: [
                "./#src/templates/theme/flowers_light/**/*.html",
                "./#src/templates/theme/flowers_light/pages/*.html"
            ]
        },
        global_flowers_light_views: {
            src: [
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ],
            dist: "./main/core/theme/flowers_light/views/global/",
            watch: [
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ]
        },
        flowers_light_js: {
            src: [
                "./#src/js/theme/global/**/*.js",
                
            ],
            dist: "./main/core/theme/flowers_light/js/",
            watch: [
                "./#src/js/theme/global/**/*.js",
            ]
        },
        flowers_light_styles: {
            src: "./#src/scss/theme/flowers_light/style.{scss,sass}",
            dist: "./main/core/theme/flowers_light/css/",
            watch: [
                "./#src/scss/theme/flowers_light/**/*.{scss,sass}",
                "./#src/scss/theme/flowers_light/**/*.{scss,sass}",
                "./#src/scss/theme/global/**/*.{scss,sass}"

                
            ]
        },
        flowers_light_change_fonts: {
            src: "./#src/scss/theme/flowers_light/fonts/**/*.{scss,sass}",
            dist: "./main/core/theme/flowers_light/css/fonts/",
            watch: [
                "./#src/scss/theme/flowers_light/fonts/**/*.{scss,sass}",
                "./#src/scss/theme/flowers_light/fonts/**/*.{scss,sass}",
                "./#src/scss/theme/fastflowers_light_theme/fonts/**/*.{scss,sass}"

                
            ]
        },
        flowers_light_scripts: {
            src: "./#src/js/theme/flowers_light/*.js",
            dist: "./main/core/theme/flowers_light/js/",
            watch: [
                "./#src/js/theme/flowers_light/**/*.js",
                "./#src/js/theme/flowers_light/**/*.js",
              
            ]
        },
        flowers_light_images: {
            src: [
                "./#src/images/theme/flowers_light/**/*.{jpg,jpeg,png,gif,tiff,svg,webp}",
                "!./#src/images/theme/flowers_light/fav/*.{jpg,jpeg,png,gif,tiff,webp}"
            ],
            dist: "./main/core/theme/flowers_light/images/",
            watch: "./#src/images/theme/flowers_light/**/*.{jpg,jpeg,png,gif,svg,tiff,webp}"
        },
        flowers_light_sprites: {
            src: "./#src/images/theme/flowers_light/sprites/*.svg",
            dist: "./main/core/theme/flowers_light/images/sprites/",
            watch: "./#src/images/theme/flowers_light/sprites/*.svg"
        },
        flowers_light_fonts: {
            src: "./#src/fonts/theme/flowers_light/**/*.{woff,woff2,ttf,TTF,otf}",
            dist: "./main/core/theme/flowers_light/fonts/",
            watch: "./#src/fonts/theme/flowers_light/**/*.{woff,woff2,ttf,TTF,otf}"
        },
        flowers_light_favicons: {
            src: "./#src/img/theme/flowers_light/fav/*.{jpg,jpeg,png,gif}",
            dist: "./main/core/img/fav/",
        },

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
                "./#src/templates/theme/global/**/*.html",
                "./#src/templates/theme/global/pages/*.html"
            ]
        },
        global_chinajs: {
            src: [
                "./#src/js/theme/global/**/*.js",
                
            ],
            dist: "./main/core/theme/china/js/",
            watch: [
                "./#src/js/theme/global/**/*.js",
            ]
        },
        chinastyles: {
            src: "./#src/scss/theme/china/style.{scss,sass}",
            dist: "./main/core/theme/china/css/",
            watch: [
                "./#src/scss/theme/china/**/*.{scss,sass}",
                "./#src/scss/theme/china/**/*.{scss,sass}",
                "./#src/scss/theme/global/**/*.{scss,sass}"
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
        'global_js',
        "styles", 
        "scripts", 
        "images", 
        "webp", 
        "sprites", 
        "fonts", 
        "favicons",
        "sushi_views",
        "global_sushi_views",
        "sushi_js",
        "sushi_styles",
        "sushi_change_fonts",
        "sushi_scripts",
        "sushi_webp", 
        "sushi_images",
        "sushi_sprites",
        "sushi_fonts",
        "sushi_favicons",
        "fast_views",
        'global_fast_views',
        "fast_js",
        "fast_styles",
        "fast_change_fonts",
        "fast_scripts",
        "fast_webp", 
        "fast_images",
        "fast_sprites",
        "fast_fonts",
        "fast_favicons",

        "flowers_light_views",
        'global_flowers_light_views',
        "flowers_light_js",
        "flowers_light_styles",
        "flowers_light_change_fonts",
        "flowers_light_scripts",
        "flowers_light_webp", 
        "flowers_light_images",
        "flowers_light_sprites",
        "flowers_light_fonts",
        "flowers_light_favicons",

        "chinaviews", 
        'global_chinaviews',
        'global_chinajs',
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
        'global_views',
        'global_js',
        "styles", 
        "scripts", 
        "images", 
        "webp", 
        "sprites", 
        "fonts", 
        "favicons",
        "sushi_views",
        "global_sushi_views",
        "sushi_js",
        "sushi_styles",
        "sushi_change_fonts",
        "sushi_scripts",
        "sushi_webp", 
        "sushi_images",
        "sushi_sprites",
        "sushi_fonts",
        "sushi_favicons",
        "fast_views",
        'global_fast_views',
        "fast_js",
        "fast_styles",
        "fast_change_fonts",
        "fast_scripts",
        "fast_webp", 
        "fast_images",
        "fast_sprites",
        "fast_fonts",
        "fast_favicons",

        "flowers_light_views",
        'global_flowers_light_views',
        "flowers_light_js",
        "flowers_light_styles",
        "flowers_light_change_fonts",
        "flowers_light_scripts",
        "flowers_light_webp", 
        "flowers_light_images",
        "flowers_light_sprites",
        "flowers_light_fonts",
        "flowers_light_favicons",
        
        "chinaviews", 
        'global_chinaviews',
        'global_chinajs',
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
    ]));

export default development;
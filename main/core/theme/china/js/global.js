
$(document).on('click','.toggle-menu',function(e){
    e.preventDefault();
    $(".menu-btn").toggleClass('menu-btn_active');
    $('.header-bottom__list').toggleClass('header-bottom__list--active')
   
   
})


$(document).on('click','.header__cat',function(e){
    e.preventDefault();
    $(".menu-btn").toggleClass('menu-btn_active');
})

$(document).on('click','.content',function(){
    
    $(".menu-btn").removeClass('menu-btn_active');
    $('.header-bottom__list').removeClass('header-bottom__list--active')

})

// .header__contacts-btn
$(document).on('click','.header__contacts-btn',function(e){
    e.preventDefault();
    $(".popup").toggleClass('popup--active');
})
$(document).on('click','.popup__overlay, .popup__closer',function(e){
    e.preventDefault();
    $(".popup").removeClass('popup--active');
})


jQuery(document).ready(function ($) {
    var url = document.location.href;
    $.each($(".header__link"), function () {
        if (this.href == url) {
        $(this).addClass('header__link--active');
        }
    });
});

jQuery(document).ready(function ($) {
    var url = document.location.href;
    $.each($(".account__top-link"), function () {
        if (this.href == url) {
        $(this).addClass('account__top-link--active');
        }
    });
});

jQuery(document).ready(function ($) {
    var url = document.location.href;
    $.each($(".blog-list__sidebar-item"), function () {
        if (this.href == url) {
        $(this).addClass('blog-list__sidebar-item--active');
        }
    });
});

$(document).ready(function(){
    var dataSpeed = $('.owl-carousel').attr('data-speed')
    var dataNav = $('.owl-carousel').attr('data-nav')
    var dataDots = $('.owl-carousel').attr('data-dots')
    var dataAutoplay = $('.owl-carousel').attr('data-autoplay')
    if (dataNav=='False'){
        dataNav=false
    } else {
        dataNav=true
    }
    if (dataDots=='False'){
        dataDots=false
    } else {
        dataDots=true
    }
    if (dataAutoplay=='False'){
        dataAutoplay=false
    } else {
        dataAutoplay=true
    }
  

    $('.sl').owlCarousel({
        items:1,
        lazyLoad:true,
        loop:true,
        animateOut: 'fadeOut',
        autoplay:dataAutoplay,
        autoplayTimeout:dataSpeed,
        autoplayHoverPause:true,
        nav:dataNav,
        dots:dataDots,
    });
})

$(document).ready(function(){
    $('.product-list--slider').owlCarousel({
        items:4,
        lazyLoad:true,
        loop:true,
        animateOut: 'fadeOut',
        autoplay:true,
        autoplayTimeout:5000,
        autoplayHoverPause:false,
        nav:false,
        dots:false, 
        responsive:{ 
            0:{
                items:1
            },
            480:{
                items:1
            },
            600:{
                items:3
            },
            1000:{
                items:4
            }
        }
    });
});


// Навигация
$(document).on('click','.header__link--drop',function(e){
    e.preventDefault();
    $('.header__dropdown').removeClass('header__dropdown--active')
    $(this).next('.header__dropdown').toggleClass('header__dropdown--active')
})
$(document).on('click','.content',function(){
    $('.header__dropdown').removeClass('header__dropdown--active')
})
$(document).on('mouseleave','.header__dropdown',function(){
    $(this).removeClass('header__dropdown--active')
})


// Поиск

$(document).on('click','.header__search',function(e){
    e.preventDefault();
    $('.search').addClass('search--active')
})
$(document).on('click','.search__closer',function(e){
    e.preventDefault();
    $('.search').removeClass('search--active')
})




// Добавление в корзину product-list__form
$(function() {
    $(document).on('submit','.product-list__form, .product-detail__form',function(e){
      var $form = $(this);
      

      $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
      }).done(function() {

        $.get( "/cart/set_delivery/1/", function() { 
            $(".cart__inner").load(location.href + " .cart__refresh");
            
            $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
            $(".header__cart-wrap").load(location.href + " .header__cart");
            $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
            $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

            $('#suggest').attr('required', 'required')
            $('#finaladress').attr('required', 'required')
            $('#finaladress').attr('name', 'address')
            $('#pickupInput').removeAttr('name')
            $('.cart__form-refresh-delivery').addClass('cart__form-refresh-delivery--active')
            $('.cart__pickup-row').removeClass('cart__pickup-row--active')
            $('#delivery_method').val('Доставка')
    
        });


        $(".cart__inner").load(location.href + " .cart__refresh");
        
        $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
        $(".header__cart-wrap").load(location.href + " .header__cart");
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        

        $form.children('button').removeClass('btn--primary')
        $form.children('button').addClass('btn--success')
        $form.children('button').html('Добавлен')
        
        function explode(){

            $form.children('button').addClass('btn--primary')
            $form.children('button').removeClass('btn--success')
            $form.children('button').html('Еще')
        }
        setTimeout(explode, 1000);

        function uxplode(){
            $form.children('button').html('В корзину')
        }
        setTimeout(uxplode, 5000);
        
      }).fail(function() {
        console.log('fail');
      });
      e.preventDefault();
    });
});


$(function() {
    $(document).on('submit','.qtybutton',function(e){
      var $form = $(this);
      $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
      }).done(function() {
        $(".cart__inner").load(location.href + " .cart__refresh");
        
        $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
        $(".header__cart-wrap").load(location.href + " .header__cart");
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        

        $form.children('button').removeClass('btn--primary')
        $form.children('button').addClass('btn--success')
        
        
        function explode(){

            $form.children('button').addClass('btn--primary')
            $form.children('button').removeClass('btn--success')
           
        }
        setTimeout(explode, 1000);

        function uxplode(){
            $form.children('button').html('В корзину')
        }
        setTimeout(uxplode, 5000);
        
      }).fail(function() {
        console.log('fail');
      });
      e.preventDefault();
    });
});

$(function() {
    $(document).on('submit','.cart__form-coupon',function(e){
      var $form = $(this);
      $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
      }).done(function() {
        $(".cart__inner").load(location.href + " .cart__refresh");
        
        $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
        $(".header__cart-wrap").load(location.href + " .header__cart");
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        $(".cart__form-coupon").load(location.href + " .cart__form-coupon-inner");
        
        
        
      }).fail(function() {
        console.log('fail');
      });
      e.preventDefault();
    });
});

//   Удаление из корзины
$(document).on('click','.cart__remove, .product-remove a',function(e){
    e.preventDefault();
    var url = $(this).attr('href')
    $.get(url, function() {
        $(".cart__inner").load(location.href + " .cart__refresh");
        
        $(".header__cart-wrap").load(location.href + " .header__cart");
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");

        
    });

    count = 0
    $('.cart__item').each(function(index){
        count = index
    })
    if (count==0) {
        // function remove(){
            $('.cart').removeClass('cart--active')
            $('.cart__form').hide()
            $('#map').hide()
            $('body').removeClass('body')

        // }
        // setTimeout(remove, 1000);
    }
});


//   Применение баллов
$(document).on('click','.cart__order-line__balls-link',function(e){
    e.preventDefault();
    var url = $(this).attr('href')
    $.get(url, function() {
        $(".cart__inner").load(location.href + " .cart__refresh");
        
        $(".header__cart-wrap").load(location.href + " .header__cart");
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
        
        $(".cart__inner").load(location.href + " .cart__refresh");
        $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
        // $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
        $(".header__cart-wrap").load(location.href + " .header__cart");
        // $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
    
    });

   
});

// Купон
$(function() {
    $(document).on('submit','.cart-coupon',function(e){
      var $form = $(this);
      $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
      }).done(function() {
        
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        

        
      }).fail(function() {
        console.log('fail');
      });
      e.preventDefault();
    });
});

// Скрол хедера
$(window).scroll(function() {
    var height = $(window).scrollTop();
    /*Если сделали скролл на 100px задаём новый класс для header*/
    if(height > 200){
        $('.header').addClass('header--hide');
        
        
    } else{
        /*Если меньше 100px удаляем класс для header*/
        $('.header').removeClass('header--hide');
              
    }
    if(height > 200){
        $('.header').addClass('header--fixed');
        
        
    } else{
        /*Если меньше 100px удаляем класс для header*/
        $('.header').removeClass('header--fixed');
       

       
    }
});


// jQuery(document).ready(function($) {
//     var url=document.location.href;
//     $.each($(".header__link"),function(){
//         if(this.href==url){
//             $(this).addClass('header__link--active');
//         }
//     });
// });



// Сортировка

$(document).on('click','.sort__title',function(){
    $(this).next('.sort__options').show()
    
});

$(document).on('mouseleave','.sort__options',function(){
    $('.sort__options').hide()
    
});

$(document).on('click','.sort__option',function(){
    var getUrl = $(this).attr("data-url")

    function setLocation(curLoc){
        try {
          history.pushState(null, null, curLoc);
          return;
        } catch(e) {}
        location.hash = '#' + curLoc;
    }

    setLocation(getUrl)

    function refresh(){
        $(".catalog__list").load(location.href + " .catalog__refresh");
        $(".catalog__sidebar").load(location.href + " .catalog__sidefresh");
    }
    setTimeout(refresh, 200);
});




// Фильтры

$(document).on('keyup','.filter__input',function(){
    // $(this).val($(this).val().replace(/[A-Za-zА-Яа-яЁё]/, ''))
    var filter = $(this).attr('data-filter')
    var key = $(this).attr('data-key')
    var getUrl = $(this).attr("data-get")

    if ($(this).val() == '') {
        var hrefUrl = '?' + key + '=' + filter + getUrl
    } else {
        var hrefUrl = '?' + key + '=' + $(this).val() + getUrl
    }
    function setLocation(curLoc){
        try {
          history.pushState(null, null, curLoc);
          return;
        } catch(e) {}
        location.hash = '#' + curLoc;
    }
    
    setLocation(hrefUrl)

    function refresh(){
        $(".catalog__list").load(location.href + " .catalog__refresh");
        
        if($(this).parent().parent().next('.filter__price-item') == true ) {

            $(".ref-max").load(location.href + " .ref-max-ref");
            
        } else if ($(this).parent().parent().prev('.filter__price-item') == true ) {
            $(".ref-min").load(location.href + " .ref-min-ref");
        }

    }

    setTimeout(refresh, 200);

    $(this).focus()
    
    

});



// счетчик

function calculate() {
	let inpt = document.querySelector('.product-detail__count-inp')
	let plus = document.querySelector('.product-detail__plus')
	let minus = document.querySelector('.product-detail__minus')
	if (plus) {
		plus.addEventListener('click', function () {
			inpt.value++
		})
	}
	if (minus) {
		minus.addEventListener('click', function () {
			inpt.value--
			if (inpt.value < 2) {
				inpt.value = 1
			}
		})
	}
}
calculate()



// Замена картинки
// .product-detail__nav-image
$(document).on('click','.product-detail__nav-image',function(){
    var image = $(this).next('div').attr('data-image');
    $('.product-detail__image').attr('src', image)
    $('.product-detail__nav-image').removeClass('product-detail__nav-image--active')
    $(this).addClass('product-detail__nav-image--active')
});




// Замена опции при выборе

$(document).on('click','.product-detail__option-value',function(){
    var image = $(this).attr('data-image');
    $('.product-detail__image').attr('src', image)

    $('.product-detail__option-value').removeClass('product-detail__option-value--active')
    $(this).addClass('product-detail__option-value--active')

    var oldPrice = parseFloat($('.product-detail__price').attr('data-price'))
    var newPrice = parseFloat($(this).attr('data-price'))
    var res = oldPrice + newPrice

    console.log(res)
    $('.product-detail__price').html(String(res)+',00₽')

    
    var newAction = $(this).attr('data-action')
    $('.product-detail__form').attr('action', newAction)
    $('.product-detail__option-value-reset').show()
    
});



// cart
// Корзина

$(document).on('click','.cart__select-active',function(){
    $(this).next('.cart__select-drop').toggleClass('cart__select-drop--active')
    $('.cart__order-layout').show()
    $(this).children('.cart__select-error').hide()
})


$(document).on('click','.cart__order-layout',function(){
    $('.cart__select-drop').removeClass('cart__select-drop--active')

    $('.cart__order-layout').hide()
})



$(document).ready(function(){

    $(document).on('click','.header__cart',function(e){
        e.preventDefault()
        $('.cart').addClass('cart--active')
        $('body').addClass('body')
        $.get( "/cart/set_delivery/1/", function() { 
            $(".cart__inner").load(location.href + " .cart__refresh");
            $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
            // $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
            $(".header__cart-wrap").load(location.href + " .header__cart");
            // $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
            $("#cart__select-drop").load(location.href + " #cart__select-drop-refresh");

            $('#suggest').attr('required', 'required')
            $('#finaladress').attr('required', 'required')
            $('#finaladress').attr('name', 'address')
            $('#pickupInput').removeAttr('name')
            $('.cart__form-refresh-delivery').addClass('cart__form-refresh-delivery--active')
            $('.cart__pickup-row').removeClass('cart__pickup-row--active')
            $('#delivery_method').val('Доставка')
            

        });
    })

    $(document).on('click','.cart__close, .cart__closer, #cancel',function(e){
        e.preventDefault()

        $.get( "/cart/set_delivery/1/", function() { 
            
            $(".cart__inner").load(location.href + " .cart__refresh");
            $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
            $('.cart__form-refresh-delivery').addClass('cart__form-refresh-delivery--active')


            $('#suggest').attr('required', 'required')
            $('#finaladress').attr('required', 'required')
            $('#finaladress').attr('name', 'address')
            $('#pickupInput').removeAttr('name')
            $('.cart__form-refresh-delivery').addClass('cart__form-refresh-delivery--active')
            $('.cart__pickup-row').removeClass('cart__pickup-row--active')
            $('#delivery_method').val('Доставка')


            // $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
            $(".header__cart-wrap").load(location.href + " .header__cart");
            // $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
           

        });

        $('.cart').removeClass('cart--active')
        $('.cart__form').hide()
        $('#map').hide()
        $('body').removeClass('body')
        $('#id_address').css('border-color', '#eaedff')
        $('#id_phone').css('border-color', '#eaedff')
        $('.cart__select-error').hide()
        // 

        
        

    })

    
    $(document).on('click','.cart__order',function(e){
        e.preventDefault()
       
        $('.cart__form').show()
        $('#map').show()
        

    })
    

    $(document).on('click','.cart__select-item--data',function(){
        $('.cart__select-item--data').removeClass('cart__select-item--active')
        $(this).addClass('cart__select-item--active')

        if ($(this).hasClass('cart__select-item-first')) {
            $('.cart__select-drop-wrap-hours').html($('.cart__select-drop-one-hidden').html())
        }
        if ($(this).hasClass('cart__select-item-second')) {
            $('.cart__select-drop-wrap-hours').html($('.cart__select-drop-two-hidden').html())
        }

        var getDay = $(this).html()
        $('#data').html(getDay)
        $('#data').attr('data-value', '1')
        var dataExit = 0

        $(".cart__select-item--time").each(function() {
            if ($(this).hasClass('cart__select-item--active')) {
                $('#time').html($(this).html())
                $('#id_datetime').val($(this).html() + ' / ' + getDay)
                dataExit = 1
            }
        });
        if (dataExit == 1) {
            $(this).parent().parent().parent('.cart__select-drop').removeClass('cart__select-drop--active')
            $(this).parent().parent().parent('.cart__select-drop').attr('data-value', '1')
            $('.cart__order-layout').hide()
        }
    })

    $(document).on('click','.cart__select-item--time',function(){
        

        $('.cart__select-item--time').removeClass('cart__select-item--active')
        $(this).addClass('cart__select-item--active')
        var getTime = $(this).html()
        $('#time').html(getTime)
        $('#time').attr('data-value', '1')

        var dataExit = 0

        $(".cart__select-item--data").each(function() {
            
            if ($(this).hasClass('cart__select-item--active')) {
                $('#data').html($(this).html())
                $('#data').attr('data-value', '1')
                $('#id_datetime').val(getTime + ' / ' + $(this).html())
                dataExit = 1
            }
        });
        if (dataExit == 1) {
            $(this).parent().parent().parent('.cart__select-drop').removeClass('cart__select-drop--active')
            $(this).parent().parent().parent().parent().attr('data-value', '1')
            $('.cart__order-layout').hide()
        }

        
    })

    $(document).on('click','.cart__select-item--card',function(){
        $('.cart__select-item--card').removeClass('cart__select-item--active')
        $(this).addClass('cart__select-item--active')
        
        var getPay = $(this).text()

        $('#pay').text(getPay)

        $('#get_pay').val(getPay)

        $('#pay_method').attr('data-value', '1')

        $(this).parent().parent('.cart__select-drop').removeClass('cart__select-drop--active')
        $('.cart__order-layout').hide()

        console.log(getPay)

    })

    $(document).on('click','.cart__select-item--pickup',function(){
        $('.cart__select-item--pickup').removeClass('cart__select-item--active')
        $(this).addClass('cart__select-item--active')
        
        var getPickup = $(this).text()

        $('#pickup_text').text(getPickup)

        $('#get_area').val(getPickup)

        $('#pickup_areas').attr('data-value', '1')

        $(this).parent('.cart__select-drop').removeClass('cart__select-drop--active')
        $('.cart__order-layout').hide()

        console.log(getPickup)

    })

})

$(document).on('click','#id_phone, #id_address',function(){
    $(this).css('border-color', '#eaedff')
})

$(function() {
    $(document).on('click','.cart__order-create',function(){
        var getOrderTime = $('#order_time').attr('data-value')
        var getTime = $('#time').attr('data-value')
        var getData = $('#data').attr('data-value')
        var payMethod = $('#pay_method').attr('data-value')
        var getPhone = $('#id_phone').val()
        var getAddress = $('#finaladress').val()

        var deliveryMethod = $('#delivery_method').val()
        if (deliveryMethod == 'Доставка') {
            $('#pickup_areas').attr('data-value', '1')
        }


        var getPhoneSubject = $('.cart__input-phone-btn').attr('data-sub')


        var pickupArea = $('#pickup_areas').attr('data-value')

        if (pickupArea=='0') {
            $('#pickup_areas').children().children('.cart__select-error').show()
        }


        if (getPhone == '') {
            $('#id_phone').css('border-color', 'red')
        } else {
            $('#id_phone').css('border-color', '#eaedff')
        }
        if (getAddress == '') {
            $('#suggest').addClass('suggest-error')
        } else {
            $('#suggest').removeClass('suggest-error')
        }
        if(getOrderTime=='0') {
            $('#order_time').children().children('.cart__select-error').show()
        } 
        if(getTime=='0') {
            $('#order_time').children().children('.cart__select-error').show()
        } 
        if(getData=='0') {
            $('#order_time').children().children('.cart__select-error').show()
        }
        if(payMethod=='0') {
            $('#pay_method').children().children('.cart__select-error').show()
        } else {
            $('#pay_method').children().children('.cart__select-error').hide()
        }
        if (getPhoneSubject=='false') {
            $('.cart__input-phone-btn-wrap').css('border-color', 'red')
        }



    });
});

$(document).on('click','.odred-done__layout, .odred-done__ok',function(e){
    e.preventDefault()
    $('.odred-done').hide()
})


$(document).on('click','.cart__form-btn',function(e){
    e.preventDefault()
    $('.cart__form-btn').removeClass('cart__form-btn--active')
    $(this).addClass('cart__form-btn--active')

    var url = $(this).attr('href')

    $.get( url, function() {
        $(".cart__inner").load(location.href + " .cart__refresh");
        $("#cart__select-drop").load(location.href + " #cart__select-drop-refresh");
       
        $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
        
    });


})

$(document).on('click','#pickup',function(e){

    
    $('.cart__form-refresh-delivery').removeClass('cart__form-refresh-delivery--active')
    $('.cart__pickup-row').addClass('cart__pickup-row--active')

    $('#suggest').removeAttr('required')
    $('#finaladress').removeAttr('required')
    $('#finaladress').removeAttr('name')

    $('#suggest').val('')
    $('#finaladress').val('')

    $('#pickupInput').attr('name', 'address')


    $(".wrap-delivery-address").load(location.href + " .wrap-delivery-address__inner");
    $('#delivery_method').val('Самовывоз')

})

$(document).on('click','#delivery',function(e){

    $('#suggest').attr('required', 'required')
    $('#finaladress').attr('required', 'required')
    $('#finaladress').attr('name', 'address')

    $('#pickup_areas').attr('data-value', '0')
    $("#pickup_areas").load(location.href + " .#pickup_areas_refresh");

    $('#pickupInput').removeAttr('name')


    $('.cart__form-refresh-delivery').addClass('cart__form-refresh-delivery--active')
    $('.cart__pickup-row').removeClass('cart__pickup-row--active')
    $('#delivery_method').val('Доставка')
    $('#get_area').val('')
    $(".wrap-delivery-address").load(location.href + " .wrap-delivery-address__inner");

})


// Карты




var deliveryArea;
var myMap;
ymaps.ready(init);

function init() {

    var city = $('#suggest').attr('data-city')
    var zones = $('#suggest').attr('data-zones')

    var suggestView=new ymaps.SuggestView(
        'suggest', {
            provider: {
            suggest: (function(request, options) {
    
                return ymaps.suggest(city + ", " + request)
                })
            }}

        );

    if (zones == 'false') {
        $(document).on('click touchend', '.ymaps-2-1-79-suggest-item' ,function(e){
            $('#finaladress').val($('#suggest').val())
        })
    } else {
        $(document).on('keyup','#suggest',function(e){
            $('#suggest').css('border-color', 'red');
            $('#finaladress').val('')
        })

        ymaps.geocode(city).then(function (res) {
            myMap = new ymaps.Map('map', {
                center: res.geoObjects.get(0).geometry.getCoordinates(),
                zoom : 12,
                controls: []

            });


            function getzones() {
                var flickerAPI = "/core/libs/delivery.json";
                $.getJSON( flickerAPI, {
                    tags: "mount rainier",
                    tagmode: "any",
                    format: "json"
                })
                .done(function( data ) {
                    var count = 0
                    $.each(data.deliverys, function(index, val) {
                        
                        freeArea = new ymaps.Polygon(
                            [
                                val.coords
                            ], {
                                hintContent: val.hintContent,
                                balloonContent: val.balloonContent,
                                balloonContentHeader: val.balloonContentHeader,
                                balloonContentBody: val.balloonContentBody,
                                balloonContentFooter: val.balloonContentFooter
                            }, {
                        
                            fillColor: val.fillColor,
                            strokeColor: val.strokeColor,
                            opacity: val.opacity
                        });
                        myMap.geoObjects.add(freeArea);
                        count+=1
                    })
                });
            };
            getzones()
            $(document).on('click touchend', '.ymaps-2-1-79-suggest-item' ,function(e){
                geocode();
                getzones()
            })
            function showError(message) {
                $('#suggest').addClass('suggest-error')
                $('#addressError').text(message)
                $('#addressError').show()
            }
            function geocode() {
                // Забираем запрос из поля ввода.
                myMap.geoObjects.removeAll()
                var request = $('#suggest').val();
                // Геокодируем введённые данные.
                ymaps.geocode(request).then(function (res) {
                    var obj = res.geoObjects.get(0),
                        error, hint;
    
                    if (obj) {
                        // Об оценке точности ответа геокодера можно прочитать тут: https://tech.yandex.ru/maps/doc/geocoder/desc/reference/precision-docpage/
                        switch (obj.properties.get('metaDataProperty.GeocoderMetaData.precision')) {
                            case 'exact':
                                break;
                            case 'number':
                            case 'near':
                            case 'range':
                                error = 'Уточните номер дома';
                                hint = 'Уточните номер дома';
                                break;
                            case 'street':
                                error = 'Уточните номер дома';
                                hint = 'Уточните номер дома';
                                break;
                            case 'other':
                            default:
                                error = 'Уточните адрес';
                                hint = 'Уточните адрес';
                        }
                    } else {
                        error = 'Адрес не найден';
                        hint = 'Уточните адрес';
                    }
    
                    // Если геокодер возвращает пустой массив или неточный результат, то показываем ошибку.
                    if (error) {
                        showError(error)
                        
                    } else {
                        // showResult(obj);
                        
                        var deliveryText = ''
                        myMap.geoObjects.each(function (item) {
                            if(item.geometry.getType() == "Polygon"){
                                if (item.geometry.contains(obj.geometry._coordinates)) {

                                    var deliveryText = item.properties._data.hintContent
                                    var deliveryPrice = item.properties._data.balloonContentFooter
                                    var sd=parseInt(deliveryPrice);
                                    $.get( "/cart/delivery_summ/"+sd+'/', function() { 
                                        $(".cart__inner").load(location.href + " .cart__refresh");
                                        
                                        $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
                                        $(".header__cart-wrap").load(location.href + " .header__cart");
                                        $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
                                        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
                            
                                        
                                
                                    });



                                    // console.log(deliveryPrice)
                                    // console.log(deliveryText)
    
                                    myGeoObject = new ymaps.GeoObject({
                                        // Описание геометрии.
                                        geometry: {
                                            type: "Point",
                                            coordinates: obj.geometry._coordinates
                                        },
                                        // Свойства.
                                        properties: {
                                            iconContent: 'Я тут',
                                        }
                                    }, {
                                        // Опции.
                                        // Иконка метки будет растягиваться под размер ее содержимого.
                                        preset: 'islands#blackStretchyIcon',
                                        // Метку можно перемещать.
                                        draggable: false
                                    })
                                    $('#suggest').removeClass('suggest-error')
                                    $('#addressError').text('')
                                    $('#addressError').hide()
                                    myMap.geoObjects.removeAll()
                                    getzones()
                                    myMap.geoObjects.add(item)
                                    myMap.geoObjects.add(myGeoObject)
                                    $('#finaladress').val($('#suggest').val())
                                    myMap.setCenter(obj.geometry._coordinates);
                                    myMap.setZoom(17);
                                    $('#suggest').css('border-color', 'green');
    
                                } else {
                                    showError('Нет доставки')
                                    $('#finaladress').val('')
                                }
    
                            }
    
                        })
                        
                        
                    }
                }, function (e) {
                    console.log(e.geometry._coordinates)
                })
    
            }
        });

    }
    
}




$(document).on('focus', '.phone' ,function(e){
    $(".phone").mask("+7 (999) 999 99-99");
})


$(".phone").on("blur", function() {
    var last = $(this).val().substr( $(this).val().indexOf("-") + 1 );
    if( last.length == 3 ) {
        var move = $(this).val().substr( $(this).val().indexOf("-") - 1, 1 );
        var lastfour = move + last;
        var first = $(this).val().substr( 0, 9 );
        $(this).val( first + '-' + lastfour );
    }
});

// Номер телефона в корзине
$(document).on('keyup', '.phone-sms' ,function(e){
    var phone = $(this).val()
    var min = phone.replace('_', '').replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('+', '')
    if (min.length == 13) {
        $('.cart__input-phone-btn').css({'display':'flex'})
        $(".get-sec").load(location.href + " .get-sec__inner");
        var secGet = $('.get-sec__inner').attr('data-timer')
        // $('.id_phone-wrap--remove').remove()
        if (secGet != '') {
            var sec = 120 - secGet
            var nowData = $('.cart__input-phone-btn').text()
            console.log(sec)
            console.log(nowData)
            if (sec > 0) {
                if (nowData == 'Подтвердить') {
                    $(".cart__input-phone-btn-wrap").countdown(redirect, sec, "Повторная отправка через <br>");
                }
            }
        }
    } else {
        $('.cart__input-phone-btn').css({'display':'none'})
    }
})


// Our countdown plugin takes a callback, a duration, and an optional message
$.fn.countdown = function (callback, duration, message) {
    // If no message is provided, we use an empty string
    message = message || "";
    // Get reference to container, and set initial content
    var container = $(this[0]).html("<small>" + message + " " + "<center>" + duration + " секунд" + "</center>" + "</small>");
    // Get reference to the interval doing the countdown
    var countdown = setInterval(function () {
        // If seconds remain
        if (--duration) {
            // Update our container's message
            container.html("<small>" + message + " " + "<center>" + duration + " секунд" + "</center>" + "</small>");
        // Otherwise
        } else {
            // Clear the countdown interval
            clearInterval(countdown);
            // And fire the callback passing our container as `this`
            callback.call(container);
        }
    // Run interval every 1000ms (1 second)
    }, 1000);
};

// Function to be called after 5 seconds
function redirect () {
    this.html('<div class="cart__input-phone-btn" data-sub="false">Отправить снова</div>');
    $('.cart__input-phone-btn').css({'display':'flex'})

    $('.phone').removeAttr('readonly');


}




// cart__input-phone-btn
$(document).on('click', '.cart__input-phone-btn' ,function(e){
    $(this).parent().css('border-color', '')
    $('#id_phone').attr('readonly', 'readonly');
    var csrf = $(this).parent().attr('data-token')
    var phone = $('.phone-get').val()
    $.ajax({
        method: "POST",
        url: "/accounts/code/",
        data: { 
            csrfmiddlewaretoken: csrf,
            phone: phone
        }
        })
      .done(function( msg ) {
        $('.cart__input-sms').show()
        $(".cart__input-phone-btn-wrap").css('padding', '0 15px')
    
        $(".cart__input-phone-btn-wrap").countdown(redirect, 120, "Повторная отправка через <br>");

      });

    
})


// Регистрация
$(document).on('click', '.user-login__btn' ,function(e){

    var csrf = $(this).parent().attr('data-token')
    var phone = $('.user-login__input-phone').val()
   
    $.ajax({
        method: "POST",
        url: "/accounts/code/",
        data: { 
            csrfmiddlewaretoken: csrf,
            phone: phone
        }
        })
      .done(function( msg ) {
        $('.user-login__sms').show()
        $(".user-login__btn").css('padding', '0 15px')
    
        $(".user-login__btn").countdown(redirect, 120, "Повторная отправка через <br>");

      });
    
})
$(document).on('keyup', '.user-login__input' ,function(e){
    var phone = $(this).val()
    var min = phone.replace('_', '').replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('+', '')
    if (min.length == 13) {
        $('.user-login__btn').css({'display':'flex'})
        $(".get-sec").load(location.href + " .get-sec__inner");
        var secGet = $('.get-sec__inner').attr('data-timer')
        // $('.id_phone-wrap--remove').remove()
        if (secGet != '') {
            var sec = 120 - secGet
            var nowData = $('.user-login__btn').text()
            console.log(sec)
            console.log(nowData)
            if (sec > 0) {
                if (nowData == 'Подтвердить') {
                    $(".user-login__btn").countdown(redirect, sec, "Повторная отправка через <br>");
                }
            }
        }
    } else {
        $('.user-login__btn').css({'display':'none'})
    }
})


$(document).on('click', '.user-login__input-sms-btn' ,function(e){
    
    var csrf = $(this).attr('data-token')
    var phone = $('.user-login__input-phone').val()
    var code = $('.user-login__code').val()
    var sms = $('.cart__form-success-sms').val()
    if (sms == 'on') {
        sms_res = 'True'
    } else {
        sms_res = 'False'
    }
    console.log(sms)

    var loc = $(this).attr('data-url')

    $.ajax({
        method: "POST",
        url: "/accounts/register/",
        data: { 
            csrfmiddlewaretoken: csrf,
            phone: phone,
            code: code,
            sms: sms_res,
        }
    }).done(function(  ) {
       

        if (loc == 'login') {
            window.location.href = "/accounts/profile/";
        }
     
        
    }).fail(function() {
        console.log('fail')
    });

    
})

// Регистрация



// cart__input-phone-btn
$(document).on('click', '.cart__input-sms-btn' ,function(e){
    
    var csrf = $(this).attr('data-token')
    var phone = $('.phone-get').val()
    var code = $('.code_value').val()
   
  

    var loc = $(this).attr('data-url')

    $.ajax({
        method: "POST",
        url: "/accounts/add/",
        data: { 
            csrfmiddlewaretoken: csrf,
            phone: phone,
            code: code
        }
    }).done(function(  ) {
        $('.code_value').css('border-color', 'green')
        $('.cart__input-sms').hide()
        $('#phone').removeAttr('readonly');
        $(".phone_refresh").load(location.href + " .phone_refresh__inner");

        $(".header__cart-wrap").load(location.href + " .header__cart");
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
        
        $(".cart__inner").load(location.href + " .cart__refresh");
        $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
        // $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
        $(".header__cart-wrap").load(location.href + " .header__cart");
        // $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

        function getPause() {
            $('#id_phone').css('border-color', 'green');
        }

        setTimeout(getPause, 1000);

        if (loc == 'login') {
            window.location.href = "/accounts/profile/";
        }
     
        
    }).fail(function() {
        $('.code_value').css('border-color', 'red')
    });

    
})


$(document).on('blur','.phone',function(){
    var last = $(this).val().substr( $(this).val().indexOf("-") + 1 );

    if( last.length == 3 ) {
        var move = $(this).val().substr( $(this).val().indexOf("-") - 1, 1 );
        var lastfour = move + last;
        var first = $(this).val().substr( 0, 9 );

        $(this).val( first + '-' + lastfour );
    }
})

// id_phone__edit
$(document).on('click','.id_phone__edit',function(){

    $.ajax({
        url: '/logout/',
        method: 'get',
        cache: false,
        success: function(){  
             
            $(".phone_refresh").load(location.href + " .phone_refresh__inner");
        }
    });

})


$(document).on('click','.hidden-content__remove',function(){

    $(".phone_refresh").load(location.href + " .phone_refresh__inner");

})


// Платежи
jQuery(document).ready(function ($) {

    var confirm_page = $('#confirm_page').attr('data-order')
    var confirm_status = $('#confirm_page').attr('data-status')
    var order_id = $('#confirm_page').attr('data-order')
    var count = 0
    if(confirm_page && confirm_status=='pending') {
            let timerId = setTimeout(function tick() {
                confirm_status = $('#confirm_page').attr('data-status')
                console.log(confirm_status)
                if (count <= 5) {
                    $(".thank").load(location.href + " .thank__refresh");
                    if (confirm_status == 'pending') {
                        timerId = setTimeout(tick, 1000); // (*)
                        count +=1
                    }
                } else {
                    $('.thank__loader').hide()
                    $('.thank__try').addClass('thank__try--active')
                }
            }, 1000);
            $.get('/order/confirm/'+order_id, function() {});
    } else if(confirm_status=='succeeded') {
        window.location.href = '/?order=True'
    }
})


jQuery(document).ready(function () {
    var pathname = window.location.href; 
    var origin   = window.location.origin;


    res = pathname.replace(origin, '')
    

    if(res == '/?order=True') {
        $('.odred-done').show()

        $(document).on('click','.odred-done__layout, .odred-done__ok',function(e){
            window.location.href = '/'
        })
    }


    
})


// Платежи


$(document).on('click','.cookie__btn',function(e){
    e.preventDefault();
   

    var csrfToken = $(this).attr('data-token')
    $.post( "/", { get_cookie: "ZcMWy~DhAiTo0@~", csrfmiddlewaretoken: csrfToken})
        
        .done(function( ) {
            $('.cookie').hide()
        });
})



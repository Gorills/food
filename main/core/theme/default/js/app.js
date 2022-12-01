
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
        $(".cart__inner").load(location.href + " .cart__refresh");
        $(".cart__form-refresh").load(location.href + " .cart__form");
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
        function remove(){
            $('.cart').removeClass('cart--active')
            $('.cart__form').hide()
            $('body').removeClass('body')

        }
        setTimeout(remove, 1000);
    }
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
// !!! Какая то хуйня
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
    })
    $(document).on('click','.cart__close, .cart__closer, #cancel',function(e){
        e.preventDefault()

        $.get( "/cart/set_delivery/1/", function() { 
            $(".cart__inner").load(location.href + " .cart__refresh");
            $(".cart__form-refresh").load(location.href + " .cart__form");
            $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
            $(".header__cart-wrap").load(location.href + " .header__cart");
            $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

        });

        $('.cart').removeClass('cart--active')
        $('.cart__form').hide()
        $('body').removeClass('body')
        $('#id_address').css('border-color', '#eaedff')
        $('#id_phone').css('border-color', '#eaedff')
        $('.cart__select-error').hide()
        $(".cart__form-refresh").load(location.href + " .cart__form");

        
        

    })

    
    $(document).on('click','.cart__order',function(e){
        e.preventDefault()
        $('.cart__form').show()
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

        $(this).parent('.cart__select-drop').removeClass('cart__select-drop--active')
        $('.cart__order-layout').hide()

        console.log(getPay)

    })

})

$(document).on('click','#id_phone, #id_address',function(){
    $(this).css('border-color', '#eaedff')
})

// $(function() {
//     $(document).on('submit','.cart__form-form',function(e){
//         var getOrderTime = $('#order_time').attr('data-value')
//         var getTime = $('#time').attr('data-value')
//         var getData = $('#data').attr('data-value')
//         var payMethod = $('#pay_method').attr('data-value')
//         var getPhone = $('#id_phone').val()
//         var getAddress = $('#id_address').val()
//         if (getPhone == '') {
//             $('#id_phone').css('border-color', 'red')
//         } else {
//             $('#id_phone').css('border-color', '#eaedff')
//         }
//         if (getAddress == '') {
//             $('#id_address').css('border-color', 'red')
//         } else {
//             $('#id_address').css('border-color', '#eaedff')
//         }
//         if(getOrderTime=='0') {
//             $('#order_time').children().children('.cart__select-error').show()
//         } 
//         if(getTime=='0') {
//             $('#order_time').children().children('.cart__select-error').show()
//         } 
//         if(getData=='0') {
//             $('#order_time').children().children('.cart__select-error').show()
//         }
//         if(payMethod=='0') {
//             $('#pay_method').children().children('.cart__select-error').show()
//         } else {
//             $('#pay_method').children().children('.cart__select-error').hide()
//         }



//         if(getOrderTime != '0' && getTime != '0' && getData != '0' && payMethod != '0' && getPhone != '' && getAddress != '') {
//             var $form = $(this);
//             $.ajax({
//                 type: $form.attr('method'),
//                 url: $form.attr('action'),
//                 data: $form.serialize()
//             }).done(function() {

//                 $(".cart__inner").load(location.href + " .cart__refresh");
//                 $(".cart__form-refresh").load(location.href + " .cart__form");
//                 $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
//                 $(".header__cart-wrap").load(location.href + " .header__cart");
//                 $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");   

//                 $('.cart').removeClass('cart--active')
//                 $('.cart__form').hide()
//                 $('body').removeClass('body')

//                 $('.odred-done').show()
                
                        
//             }).fail(function() {
//                 console.log('fail');
//             });
//         }
//         e.preventDefault();
//     });
// });

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
       
        $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
        
    });


})

$(document).on('click','#pickup',function(e){

    
    $('#delivery_method').val('Самовывоз')
    var htmlReplace = $('.cart__order-pickup-inner-html').html()

    // console.log(htmlReplace)

    $('.cart__form-refresh-delivery').html(htmlReplace)

})

$(document).on('click','#delivery',function(e){

    $(".cart__form-refresh-delivery").load(location.href + " .cart__form-refresh-delivery-inner");   
    $('#delivery_method').val('Доставка')

})


var count_id_address = 0
$(document).on('focus','#id_address',function(){

    var city = $(this).attr('data-city')
    if (count_id_address == 0) {
        ymaps.ready(init);
        function init(){
            
            var suggestView=new ymaps.SuggestView(
            'id_address', {
                provider: {
                  suggest: (function(request, options) {
          
                    return ymaps.suggest(city + ", " + request)
                    })
                  }}

                )
            suggestView.events.add('select',function(event){
                var selected=event.get('item').value;
                ymaps.geocode(selected,{
                    results:1
                }).then(function(res){
                    return ymaps.geocode(res.geoObjects.get(0).geometry.getCoordinates(),{
                        kind:'district',
                        results:10
                    }).then(function(res){
                        var founded=res['metaData']['geocoder']['found'];
                        $('label.suggest .description').html("");
                        for(i=0;i<=founded-1;i++){
                            var info=res.geoObjects.get(i).properties.getAll();
                            console.log(info);
                            var name=info['name'];
                            if(name.search('район')!=-1){
                                name=name.replace(' район','');
                                console.log(name);
                            }
                        }
                    });
                });
            });
        //установка смещения блока подсказок по вертикали
        document.getElementsByTagName('ymaps')[0].style.top = document.getElementsByTagName('ymaps')[0].style.top.match(/d+/)*1 + 5 + 'px';
        //установка смещения блока подсказок по горизонтали
        document.getElementsByTagName('ymaps')[0].style.left = document.getElementsByTagName('ymaps')[0].style.left.match(/d+/)*1 - 1 + 'px';
        } 
    }
    count_id_address +=1 
})







// ymaps.ready(init);
// function init() {
//     var myMap;
    
//     ymaps.geolocation.get().then(function (res) {
//         var mapContainer = $('#map'),
//             bounds = res.geoObjects.get(0).properties.get('boundedBy'),
//             // Рассчитываем видимую область для текущей положения пользователя.
//             mapState = ymaps.util.bounds.getCenterAndZoom(
//                 bounds,
//                 [10, 10]
//             );
            
//         createMap(mapState);

        
//     }, function (e) {
//         // Если местоположение невозможно получить, то просто создаем карту.
//         createMap({
//             center: [55.751574, 37.573856],
//             zoom: 2
//         });
//     });
    
//     function createMap (state) {
        
//         var myMap = new ymaps.Map('map', state),

//             deliveryPoint = new ymaps.GeoObject({
//                 geometry: {type: 'Point'},
//                 properties: {iconCaption: 'Адрес'}
//             }, {
//                 preset: 'islands#blackDotIconWithCaption',
//                 draggable: true,
//                 iconCaptionMaxWidth: '215'
//             }),
//             searchControl = myMap.controls.get('searchControl');
//         searchControl.options.set({noPlacemark: true, placeholderContent: 'Введите адрес доставки'});
//         myMap.geoObjects.add(deliveryPoint);
//         // myMap.controls.remove('zoomControl');
//         // myMap.controls.remove('searchControl');
        
//         function onZonesLoad(json) {
//             // Добавляем зоны на карту.
//             var deliveryZones = ymaps.geoQuery(json).addToMap(myMap);
//             // Задаём цвет и контент балунов полигонов.
//             deliveryZones.each(function (obj) {
//                 obj.options.set({
//                     fillColor: obj.properties.get('fill'),
//                     fillOpacity: obj.properties.get('fill-opacity'),
//                     strokeColor: obj.properties.get('stroke'),
//                     strokeWidth: obj.properties.get('stroke-width'),
//                     strokeOpacity: obj.properties.get('stroke-opacity')
//                 });
//                 obj.properties.set('balloonContent', obj.properties.get('description'));
//             });



//             // Проверим попадание результата поиска в одну из зон доставки.
//             searchControl.events.add('resultshow', function (e) {
//                 highlightResult(searchControl.getResultsArray()[e.get('index')]);
                
//             });

            
//             // Проверим попадание метки геолокации в одну из зон доставки.
//             myMap.controls.get('geolocationControl').events.add('locationchange', function (e) {
//                 highlightResult(e.get('geoObjects').get(0));
//             });

//             // При перемещении метки сбрасываем подпись, содержимое балуна и перекрашиваем метку.
//             deliveryPoint.events.add('dragstart', function () {
//                 deliveryPoint.properties.set({iconCaption: '', balloonContent: ''});
//                 deliveryPoint.options.set('iconColor', 'black');
//             });

//             // По окончании перемещения метки вызываем функцию выделения зоны доставки.
//             deliveryPoint.events.add('dragend', function () {
//                 highlightResult(deliveryPoint);
//             });

//             function highlightResult(obj) {
//                 // Сохраняем координаты переданного объекта.
//                 var coords = obj.geometry.getCoordinates(),
//                 // Находим полигон, в который входят переданные координаты.
//                     polygon = deliveryZones.searchContaining(coords).get(0);

//                 if (polygon) {
//                     // Уменьшаем прозрачность всех полигонов, кроме того, в который входят переданные координаты.
//                     deliveryZones.setOptions('fillOpacity', 0.2);
//                     polygon.options.set('fillOpacity', 0.4);
//                     // Перемещаем метку с подписью в переданные координаты и перекрашиваем её в цвет полигона.
//                     deliveryPoint.geometry.setCoordinates(coords);
//                     deliveryPoint.options.set('iconColor', polygon.properties.get('fill'));
//                     // Задаем подпись для метки.
//                     if (typeof(obj.getThoroughfare) === 'function') {
//                         setData(obj);
//                     } else {
//                         // Если вы не хотите, чтобы при каждом перемещении метки отправлялся запрос к геокодеру,
//                         // закомментируйте код ниже.
//                         ymaps.geocode(coords, {results: 1}).then(function (res) {
//                             var obj = res.geoObjects.get(0);
//                             setData(obj);
//                         });
//                     }
//                 } else {
//                     // Если переданные координаты не попадают в полигон, то задаём стандартную прозрачность полигонов.
//                     deliveryZones.setOptions('fillOpacity', 0.4);
//                     // Перемещаем метку по переданным координатам.
//                     deliveryPoint.geometry.setCoordinates(coords);
//                     // Задаём контент балуна и метки.
//                     deliveryPoint.properties.set({
//                         iconCaption: 'Нет доставки',
//                         balloonContent: 'Cвяжитесь с оператором',
//                         balloonContentHeader: ''
//                     });
//                     // Перекрашиваем метку в чёрный цвет.
//                     deliveryPoint.options.set('iconColor', 'black');
//                 }

//                 function setData(obj){
//                     var address = [obj.getThoroughfare(), obj.getPremiseNumber(), obj.getPremise()].join(' ');
//                     if (address.trim() === '') {
//                         address = obj.getAddressLine();
//                     }
//                     var price = polygon.properties.get('description');
//                     price = price.match(/<strong>(.+)<\/strong>/)[1];
//                     deliveryPoint.properties.set({
//                         iconCaption: address,
//                         balloonContent: address,
//                         balloonContentHeader: price
//                     });
//                 }
//             }
//         }
        
//         $.ajax({
//             url: 'core/libs/data.geojson',
//             dataType: 'json',
//             success: onZonesLoad
//         });

//     }
// }



$(document).on('click', '.phone' ,function(e){
    $(".phone").mask("+7 (999) 99-99-999");

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

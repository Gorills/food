// Загрузка опций
$(document).ready(function() {
    // Находим все элементы с классом product-options-popup__refresh
    $('.product-options-popup__refresh').each(function() {
        var $this = $(this);
        var productId = $this.data('id'); // Предполагается, что идентификатор продукта хранится в атрибуте data-product-id

        // Загружаем данные с другой страницы по URL /catalog/products/product_options/<id>
        $.get('/catalog/products/product_options/' + productId, function(data) {
            // Загруженные данные помещаем внутрь элемента
            $this.html(data);
        });
    });
});



function updateMinDelivery() {

    $('.minimum-bar__wrap').load(location.href + ' .minimum-bar__refresh', function() {
        var dataWidth = $('.minimum-bar__refresh').data('width');
        
        $('.minimum-bar__bar').css('width', dataWidth)
    });
    
    
}

$(document).ready(function() {
    updateMinDelivery()
    
});




jQuery(document).ready(function () {
    $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
});


// Функция для обновления отступа сверху у .content
function updateContentMargin() {
    var headerHeight = $('header').outerHeight(); // Получаем высоту header
    $('.content').css('margin-top', headerHeight); // Задаем отступ сверху для .content
  }

  function updateVideoHeigth() {
    var headerHeight = $('.sl__img').outerHeight(); // Получаем высоту header
    $('.sl__video').css('height', headerHeight); // Задаем высоту для .video
  }

  function updateVideoHeigthMobile() {
    if ($(window).width() <= 480) {
      var headerHeight = $('.sl__img-mobile').outerHeight(); // Получаем высоту header
      $('.sl__video').css('height', headerHeight); // Задаем высоту для .video
    }
  }


$(document).ready(function() {
    updateContentMargin()
    // Вызываем функцию при загрузке страницы и при изменении размеров окна
    $(window).on('load resize', function() {
      updateContentMargin();
      updateVideoHeigth();
      updateVideoHeigthMobile();
    });
  });
  
  

  

function loadCartData() {
    var cart_form = 'false'
    var map_show = 'false';
    var cart_active = 'false';
    

    if ($('.cart').hasClass('cart--active')) {
        cart_active = 'true'
    } else {
        cart_active = 'false'
    }
    if ($('#map').is(':hidden')) {
        map_show = 'false'
    } else {
        map_show = 'true'
    }
    if ($('.cart__form').is(':hidden')) {   
        cart_form = 'false'
    }  else {
        cart_form = 'true'
    }
    
    $('#cartData').load('/cart/ .cart', function() {
        if (cart_active == 'true') {
            $(this).find('.cart').addClass('cart--active');
        }
       
        
        if (cart_form == 'true') {
            $(this).find('.cart__form').show()
        }
        if (map_show == 'true') {
            $(this).find('#map').show()
            
        } 

        grecaptcha.ready(function() {
            var grecaptcha_execute = function() {
                grecaptcha.execute('6LfRKycbAAAAAEjQi1qQlqSWSJe1FYX_cXNgMNVf', {action: 'homepage'}).then(function(token) {
                    document.querySelectorAll('input.django-recaptcha-hidden-field').forEach(function(value) {
                        value.value = token;
                    });
                    // Перезагрузка страницы
                    // location.reload();
                });
            };
            grecaptcha_execute();
            setInterval(grecaptcha_execute, 120000);
        });
    });
}


$(document).on('click','.header-bottom__link',function(){
    $('.header-bottom__list').removeClass('header-bottom__list--active')
});





$(document).on('click','.product-detail__nav-image',function(e){
    e.preventDefault();
    
    var image = $(this).next().attr('data-image')
    
    console.log(image)
   
    $('.product-detail__image').attr('src',image)
})



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
        margin:20,
        
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



var dataLayer = window.dataLayer || [];
function addCart(id, name, price, category, quantity) {
    
    dataLayer.push({
        "ecommerce": {
            "currencyCode": "RUB",
            "add": {
                "products": [
                    {
                        "id": id,
                        "name": name,
                        "price": price,
                        "category": category,
                        "quantity": quantity
                    }
                ]
            }
        }
    })
}

function removeCart(id, name, price, category, quantity) {
    dataLayer.push({
        "ecommerce": {
            "currencyCode": "RUB",
            "remove": {
                "products": [
                    {
                        "id": id,
                        "name": name,
                        "price": price,
                        "category": category,
                        "quantity": quantity
                    }
                ]
            }
        }
    })
}



// Добавление в корзину product-list__form
$(function() {
    $(document).on('submit', '.product-list__form, .product-detail__form', function(e) {
      e.preventDefault();
  
      var $form = $(this);
      var id = $form.data('id');
      var name = $form.data('name');
      var price = $form.data('price');
      var category = $form.data('category');
      var quantity = $form.data('quantity');
  
      $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
      })
      .done(function() {
        
          refreshElements();
          $('#suggest').attr('required', 'required');
          $('#finaladress').attr('required', 'required').attr('name', 'address');
          $('#pickupInput').removeAttr('name');
          $('.cart__form-refresh-delivery').addClass('cart__form-refresh-delivery--active');
          $('.cart__pickup-row').removeClass('cart__pickup-row--active');
          $('#delivery_method').val('Доставка');
          $('.product-detail__button').addClass('btn--success');
          updateMinDelivery();
       
  
        
  
        $form.children('button').removeClass('btn--primary').addClass('btn--success').html('Добавлен');
        $('.product-detail__button').removeClass('btn--primary').addClass('btn--success').html('Добавлен');
  
        setTimeout(function() {
          $form.children('button').addClass('btn--primary').removeClass('btn--success').html('Еще');
          $('.product-detail__button').addClass('btn--primary').removeClass('btn--success').html('В корзину');
        }, 1000);
  
        setTimeout(function() {
          $form.children('button').html('В корзину');
        }, 5000);
  
        if (dataLayer) {
          addCart(id, name, price, category, quantity);
        }
      })
      .fail(function() {
        console.log('fail');
      });
  
      function refreshElements() {
        
        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
        updateMinDelivery()
        
      }
    });
  });
  


$(function() {
    $(document).on('submit','.qtybutton',function(e){
      var $form = $(this);
      
      var id = $(this).attr('data-id')
      var name = $(this).attr('data-name')
      var price = $(this).attr('data-price')
      var category = $(this).attr('data-category')
      var quantity = $(this).attr('data-quantity')

      $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
      }).done(function() {
        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
        $('.cart__inner').load('/cart/ .cart__refresh', function() {});
        $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
        $('.cart__deliv-method-wrap').load('/cart/ .cart__deliv-method', function() {});
        $('.cart-detail-wrap').load('/cart/ .cart-detail-wrap__refresh', function() {});
        updateMinDelivery()
        
       
        

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

        if (dataLayer) {
            if ($form.attr('action').indexOf('minus') > -1) {
                removeCart(id, name, price, category, quantity)
            } else if ($form.attr('action').indexOf('plus') > -1) {
                addCart(id, name, price, category, quantity)
            }
            
        }
        
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
        $('.cart__inner').load('/cart/ .cart__refresh', function() {});
        $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});

        $('.cart__form-refresh').load('/cart/ .cart__form', function() {});
        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
        updateMinDelivery()
        
        
        
        
      }).fail(function() {
        console.log('fail');
      });
      e.preventDefault();
    });
});

// //   Удаление из корзины
// $(document).on('click','.cart__remove, .product-remove a',function(e){
//     e.preventDefault();
//     var id = $(this).attr('data-id')
//     var name = $(this).attr('data-name')
//     var price = $(this).attr('data-price')
//     var category = $(this).attr('data-category')
//     var quantity = $(this).attr('data-quantity')

//     var url = $(this).attr('href')
//     $.get(url, function() {
     
        
//         $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
//         $('.cart__inner').load('/cart/ .cart__refresh', function() {});
//         $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
//         $('.cart__deliv-method-wrap').load('/cart/ .cart__deliv-method', function() {});
//         $('.cart-detail-wrap').load('/cart/ .cart-detail-wrap__refresh', function() {});
//         updateMinDelivery()



//         // $('.cart__form-refresh').load('/cart/ .cart__form', function() {});
//         removeCart(id, name, price, category, quantity) 
//         updateMinDelivery()
//     });

//     count = 0
//     $('.cart__item').each(function(index){
//         count = index
//     })
//     if (count==0) {
//         // function remove(){
//             $('.cart').removeClass('cart--active')
//             $('.cart__form').hide()
//             $('#map').hide()
//             $('body').removeClass('body')

//         // }
//         // setTimeout(remove, 1000);
//     }
// });


//   Применение баллов
$(document).on('click','.cart__order-line__balls-link',function(e){
    e.preventDefault();
    var url = $(this).attr('href')
    $.get(url, function() {
        
        
        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
        $('.cart__inner').load('/cart/ .cart__refresh', function() {});
        $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
        
        
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
        
        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
        $('.cart__inner').load('/cart/ .cart__refresh', function() {});
        $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
        updateMinDelivery()

        
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
        updateContentMargin();
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
    const inpt = document.querySelector('.product-detail__count-inp');
    const plus = document.querySelector('.product-detail__plus');
    const minus = document.querySelector('.product-detail__minus');
    const quantity = document.querySelector('.product-detail__form');
    
    if (plus) {
        plus.addEventListener('click', function() {
            inpt.value++;
            quantity.setAttribute('data-quantity', inpt.value);
            $('.options_btn').attr('data-quantity', inpt.value);
        });
    }

    if (minus) {
        minus.addEventListener('click', function() {
            inpt.value--;
            if (inpt.value < 1) {
                inpt.value = 1;
            }
            quantity.setAttribute('data-quantity', inpt.value);
            $('.options_btn').attr('data-quantity', inpt.value);

        });
    }
}

calculate();



$(document).on('click','.product-options-popup__minus',function(){
    var $parent = $(this).closest('.product-options-popup__inner');
    var value = $parent.find('.product-options-popup__count-inp').val();
    
    value--;
    if (value < 1) {
        value = 1;
    }
    $parent.find('.product-options-popup__count-inp').val(value);
    $parent.find('.btn-wrap').attr('data-quantity', value);
});
$(document).on('click','.product-options-popup__plus',function(){
    var $parent = $(this).closest('.product-options-popup__inner');
    var value = $parent.find('.product-options-popup__count-inp').val();
    
    value++;
    
    $parent.find('.product-options-popup__count-inp').val(value);
    $parent.find('.btn-wrap').attr('data-quantity', value);
});






$(document).on('click','.option_setup',function(e){
    e.preventDefault();
    var $parent = $(this).parents('.product-list__item');
   
    var popup = $parent.find('.product-options-popup');
    popup.toggleClass('product-options-popup--active')

    
    $('body').addClass('body');
   
})


$(document).on('click','.product-options-popup__closer, .product-options-popup__layout',function(e){
    e.preventDefault();
    $(this).parents('.product-options-popup').removeClass('product-options-popup--active')
    $('body').removeClass('body');

})




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
        
        $('#cartData').load('/cart/ .cart', function() {
           
            $(this).find('.cart').addClass('cart--active');
            
            
    
        });

        $('body').addClass('body')
        // $.get( "/cart/set_delivery/1/", function() {});
    })

    

    $(document).on('click','#cancel',function(e){
        e.preventDefault()

        // $('#cartData').html('')
        $('.cart__form').css("display", "none")
        $('.cart__inner').load('/cart/ .cart__refresh', function() {});
        // $.get( "/cart/set_delivery/1/", function() {});
        // $('body').removeClass('body')
    })

    $(document).on('click','.cart__order',function(e){
        e.preventDefault()
        $('.cart__form').show()
        $('#map').show()
        loadCartData() 
    })
    

    $(document).on('click','.cart__select-item--data',function(){

        var id = $(this).attr('data-id');
        console.log(id)

        $('.cart__select-drop-wrap-hours').removeClass('cart__select-drop-wrap-hours--active')

        $('#time-'+id).addClass('cart__select-drop-wrap-hours--active')



        $('.cart__select-item--time').removeClass('cart__select-item--active')
        $('.cart__select-item--data').removeClass('cart__select-item--active')
        $('#id_datetime').val('')
        $('#time').html('')

        $(this).addClass('cart__select-item--active')

        if ($(this).hasClass('cart__select-item-first')) {
            $('.cart__select-drop-wrap-hours').html($('.cart__select-drop-one-hidden').html())
        }
        if ($(this).hasClass('cart__select-item-second')) {
            $('.cart__select-drop-wrap-hours').html($('.cart__select-drop-two-hidden').html())
        }

        var getDay = $(this).html()
        $('#data').html(getDay)
        $('#data').attr('data-value', '0')
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

        // if (getPay.toLowerCase().includes("наличными")) {
        //     $('#pay_change').show()
        // } else {
        //     $('#pay_change').hide()
        // }




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
        var getName = $('#id_name').val()
        var getAddress = $('#finaladress').val()
        var getZones = $('#suggest').attr('data-zones')

        var deliveryMethod = $('#delivery_method').val()
        if (deliveryMethod == 'Доставка') {
            $('#pickup_areas').attr('data-value', '1')
        }


        var getPhoneSubject = $('.cart__input-phone-btn').attr('data-sub')


        var pickupArea = $('#pickup_areas').attr('data-value')

        if (pickupArea=='0') {
            $('#pickup_areas').children().children('.cart__select-error').show()
        }

        if (getName == '') {
            $('#id_name').css('border-color', 'red')
        } else {
            $('#id_name').css('border-color', 'var(--color-cart-border)')
        }

        if (getPhone == '') {
            $('#id_phone').css('border-color', 'red')
        } else {
            $('#id_phone').css('border-color', 'var(--color-cart-border)')
        }
        if (getAddress == '') {
            $('#suggest').addClass('suggest-error')
            $('.cart__form-delivery-in-session-ref').addClass('cart__form-delivery-in-session-ref--error')
        } else {
            $('#suggest').removeClass('suggest-error')
            $('.cart__form-delivery-in-session-ref').removeClass('cart__form-delivery-in-session-ref--error')
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
    $('#delivery_method').val('Самовывоз')

    $('.minimum-bar__wrapper').load(location.href + ' .minimum-bar', function() {
        updateMinDelivery()
    });


    var url = $(this).attr('href')

    $.get( url, function() {
        loadCartData()
        
    });

})

$(document).on('click','#delivery',function(e){

    $('#suggest').attr('required', 'required')
    $('#finaladress').attr('required', 'required')
    $('#finaladress').attr('name', 'address')

    $('#pickup_areas').attr('data-value', '0')
    

    $('#pickupInput').removeAttr('name')


    $('.cart__form-refresh-delivery').addClass('cart__form-refresh-delivery--active')
    $('.cart__pickup-row').removeClass('cart__pickup-row--active')
    $('#delivery_method').val('Доставка')
    $('#get_area').val('')
    var url = $(this).attr('href')

    $('.minimum-bar__wrapper').load(location.href + ' .minimum-bar', function() {
        updateMinDelivery()
    });
    


    $.get( url, function() {
        loadCartData()
        
    });

})


// Карты










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
            // console.log(sec)
            // console.log(nowData)
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
    
    let csrf = $(this).attr('data-token')
    let phone = $('.user-login__input-phone').val()
    let code = $('.user-login__code').val()
    let sms = $('.cart__form-success-sms').val()
    if (sms == 'on') {
        sms_res = 'True'
    } else {
        sms_res = 'False'
    }
    
    let order = JSON.parse(localStorage.getItem('order'));
    order.phone = phone

    localStorage.setItem('order', JSON.stringify(order));

    let loc = $(this).attr('data-url')

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
        

        $('.phone_refresh').load('/cart/ .phone_refresh__inner', function() {});
       

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
             
            
            $('.phone_refresh').load('/cart/ .phone_refresh__inner', function() {});

        }
    });

})


$(document).on('click','.hidden-content__remove',function(){

    $('.phone_refresh').load('/cart/ .phone_refresh__inner', function() {});


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




// Платежи


$(document).on('click','.cookie__btn',function(e){
    e.preventDefault();
   

    var csrfToken = $(this).attr('data-token')
    $.post( "/", { get_cookie: "ZcMWy~DhAiTo0@~", csrfmiddlewaretoken: csrfToken})
        
        .done(function( ) {
            $('.cookie').hide()
        });
})




// .combo

$(document).on('click','.open-combo',function(e){
    e.preventDefault();

    $(this).closest('.product-list__item').find('.combo-popup').addClass('combo-popup--active')
    

})

$(document).on('click','.combo-popup__closer, .combo-popup__layout',function(e){
    e.preventDefault();
    $('.combo-popup').removeClass('combo-popup--active')

})

$(document).ready(function() {
    $('.combo-popup__item-item').click(function() {

      const itemRow = $(this).closest('.combo-popup__item-row');
      const itemItemsInRow = itemRow.find('.combo-popup__item-item');
      itemItemsInRow.removeClass('combo-popup__item-item--active');
      var dataId = $(this).attr('data-id');
      var price = $(this).attr('data-price');
      $(this).parent().parent().attr('data-check', dataId);
      $(this).parent().parent().attr('data-price', price);
      $(this).addClass('combo-popup__item-item--active');
      var dataCheck = 0;
      var count = 0;
      var itemSumm = 0;

      var comboPopup = $(this).closest('.combo-popup');
      comboPopup.find('.combo-popup__parent_list').each(function() {
        if($(this).attr('data-check') != '') {
          dataCheck ++;
        } 
        count++;
        var pr = parseFloat($(this).attr('data-price'));
        itemSumm += pr;
      });

      var summPrice = parseFloat(comboPopup.find('.combo-popup__summ').attr('data-price'));
      var quantity = parseFloat(comboPopup.find('.counter__input').val());
      itemSumm += summPrice;

      var res = itemSumm*quantity + ' ₽';
      
      if (dataCheck == count) {
        comboPopup.find('.combo-popup__btn').addClass('combo-popup__btn--active');
      }

      products = '';


      comboPopup.find('.combo-popup__parent_list').each(function() {
        if($(this).attr('data-check') != '') {
                dataCheck ++;
                products += $(this).attr('data-check') + ','
            } 
            count++;
    
            
            
        
     
        });

    var prod = products.slice(0, -1);
    comboPopup.find('.btn-wrap').attr('data-optionsid', prod).attr('data-price', itemSumm);
    comboPopup.find('.combo-popup__summ').text(res);

        

    });
  
});




  




// header__subdomain-check

$(document).on('click','.header__subdomain-check',function(e){
    e.preventDefault();
    $('.header__subdomain-drop').toggleClass('header__subdomain-drop--active');
})

$(document).on('click','.content',function(){
   
    $('.header__subdomain-drop').removeClass('header__subdomain-drop--active');
})









// $('#finaladress').attr('required', 'required').attr('name', 'address');


$(document).on('input','#suggest',function(){
    var getVal = $(this).val();

    $('#finaladress').attr('required', 'required').attr('name', 'address');

    $('#finaladress').val(getVal);

})



$(document).on('hover','.header__cart-no-active::after',function(){
  
    $('.header__cart-no-active-popup').addClass('header__cart-no-active-popup--active')
})




// Настройка адреся доставки в сессии
$(document).on('click','.check-delivery__overlay',function(){    

    $('.check-delivery__inner').css('transform', 'scale(1.05)');

    setTimeout(function(){
        $('.check-delivery__inner').css('transform', 'scale(1)');
    }, 100)


})



$(document).on('click','.cart__form-delivery-in-session-ref',function(e){
    e.preventDefault();
    $('.setup-address').addClass('setup-address--active')
    ymaps.ready(init);

})




$(document).on('click','.check-delivery__item--pickup',function(){
    $.get("/cart/set_delivery/0/", function() {});
    $('.check-delivery').hide();

    $('.minimum-bar__wrapper').load(location.href + ' .minimum-bar', function() {
        updateMinDelivery()
    });
    
    
})
$(document).on('click','.check-delivery__item--delivery-nozones',function(){
    $.get("/cart/set_delivery/1/", function() {});
    $('.check-delivery').hide();

    $('.minimum-bar__wrapper').load(location.href + ' .minimum-bar', function() {
        updateMinDelivery()
    });
    
})






function replaceDesc(context) {
    var active = context.closest('.product-list__item').find('.constructor-popup__radio-item--active');
    var res = '';
    active.each(function() {
        res += $(this).data('desc') + ', ';
    });
    context.next('.constructor-popup').find('.constructor-popup__structure').text(res.slice(0, -2));
    context.closest('.constructor-popup').find('.constructor-popup__structure').text(res.slice(0, -2));
}

function replaceImg(context) {
    var image = context.data('image');
    if (image) {
        context.closest('.constructor-popup').find('.constructor-popup__image').attr('src', image);
    } else {
        var image_replace = context.closest('.constructor-popup').find('.constructor-popup__image').data('image');
        context.closest('.constructor-popup').find('.constructor-popup__image').attr('src', image_replace);
    }
}

function checkMinIngred(context) {
    var minIngr = context.attr('data-min');
    var items = context.find('.constructor-popup__checkbox-item');

    var items_count = context.find('.constructor-popup__checkbox-item--active').length;

    console.log(items_count)

    count = 0

    items.each(function() {
        var max = $(this).data('max');

        var active = $(this).closest('.constructor-popup__checkbox-row').find('.constructor-popup__checkbox-item--active').length;
        


        if (active >= max) {
            $(this).closest('.constructor-popup__checkbox-row').find('.constructor-popup__checkbox-item').not(".constructor-popup__checkbox-item--active").addClass('deactivate')

        } else {
            
            $(this).closest('.constructor-popup__checkbox-row').find('.constructor-popup__checkbox-item').removeClass('deactivate')
        }
        
        if (count < minIngr) {
            if($(this).hasClass('deactivate') || $(this).hasClass('deactivate-ingredient')) {
                return
            } else {
                $(this).addClass('constructor-popup__checkbox-item--active')
                count += 1
            }
            
        }
    })

}



function unique(list) {
    var result = [];
    $.each(list, function(i, e) {
      if ($.inArray(e, result) == -1) result.push(e);
    });
    return result;
  }

function countPrice(context) {
    var default_price = context.closest('.product-list__item').find('.constructor-popup').data('price');

    var_radio_price = 0
    var_checkbox_price = 0

    var all_radio = context.closest('.constructor-popup').find('.constructor-popup__radio-item--active');
    var all_checkbox = context.closest('.constructor-popup').find('.constructor-popup__checkbox-item--active');

    var all_id = ''
    all_radio.each(function() {
        var_radio_price += parseInt($(this).data('price'));
        all_id += $(this).data('id') + ','
    })
    all_checkbox.each(function() {
        var_checkbox_price += parseInt($(this).data('price'));
        all_id += $(this).data('id') + ','
    })

    res_id = all_id.slice(0, -1);
    console.log(res_id)

    

    context.find('.btn-wrap').attr('data-optionsid',res_id)

    res = default_price + var_radio_price + var_checkbox_price

    context.find('.constructor-popup__price').text(res)
    context.find('.btn-wrap').attr('data-price',res)

    return res    
}

function findNoIngr(context) {

    var all_no_ingridient_radio = context.closest('.constructor-popup').find('.constructor-popup__radio-item--active');
    var all_no_ingridient_checkbox = context.closest('.constructor-popup').find('.constructor-popup__checkbox-item--active');
    
    no_list = []
    all_no_ingridient_radio.each(function() {
        var no_ing = $(this).data('noingridient');
        // Перебираем все элементы с атрибутом data-id
        // Проверяем, является ли dataIdString строкой
        var dataIdArray;
        if (typeof no_ing === 'string') {

            dataIdArray = no_ing.split(',').map(function(item) {
                no_list.push(parseInt(item, 10));
            });

        } else if (no_ing) {
            // Если не является, создаем массив с одним элементом
            no_list.push(parseInt(no_ing, 10));
        }
    })
    all_no_ingridient_checkbox.each(function() {
        var no_ing = $(this).data('noingridient');
        // Перебираем все элементы с атрибутом data-id
        // Проверяем, является ли dataIdString строкой
        var dataIdArray;
        if (typeof no_ing === 'string') {

            dataIdArray = no_ing.split(',').map(function(item) {
                no_list.push(parseInt(item, 10));
            });

        } else if (no_ing) {
            // Если не является, создаем массив с одним элементом
            no_list.push(parseInt(no_ing, 10));
        }
    })

    no_list = unique(no_list)

    

    var radio_id = context.closest('.constructor-popup').find('.constructor-popup__radio-item');
    var checkbox_id = context.closest('.constructor-popup').find('.constructor-popup__checkbox-item');
    var foundIds = []; // Создаем массив для отслеживания найденных id

    radio_id.each(function() {
        var currentId = $(this).data('id');
        $(this).removeClass('deactivate-ingredient')
        // Проверяем, был ли этот ID уже найден ранее
        if ($.inArray(currentId, foundIds) === -1) {
            if ($.inArray(currentId, no_list) !== -1) {
                if ($(this).hasClass('constructor-popup__radio-item--active')) {
                    // Ищем предыдущий элемент с классом .constructor-popup__radio-item
                    var prevRadioItem = $(this).prev('.constructor-popup__radio-item');
                    // Если предыдущий элемент не найден, ищем следующий элемент
                    if (prevRadioItem.length === 0) {
                        prevRadioItem = $(this).next('.constructor-popup__radio-item');
                    }
                    // Теперь у вас есть либо предыдущий, либо следующий элемент
                    if (prevRadioItem.length > 0) {
                        // Ваш код для работы с prevRadioItem
                        prevRadioItem.addClass('constructor-popup__radio-item--active');
                    } else {
                        console.log('Предыдущий и следующий элементы не найдены.');
                    }

                }
                $(this).addClass('deactivate-ingredient')
                $(this).removeClass('constructor-popup__radio-item--active')

            }

            // Добавляем найденный ID в массив foundIds
            foundIds.push(currentId);
        }
    });

    checkbox_id.each(function() {
        var currentId = $(this).data('id');
        $(this).removeClass('deactivate-ingredient')
        // Проверяем, был ли этот ID уже найден ранее
        if ($.inArray(currentId, foundIds) === -1) {
            if ($.inArray(currentId, no_list) !== -1) {
                
                $(this).addClass('deactivate-ingredient')
                $(this).removeClass('constructor-popup__checkbox-item--active')

            }

            // Добавляем найденный ID в массив foundIds
            foundIds.push(currentId);
        }
    })

    var first_radio = context.closest('.constructor-popup').find('.constructor-popup__radio').first();
    var dirst_radio_item = first_radio.find('.constructor-popup__radio-item');
    dirst_radio_item.each(function() {
        $(this).removeClass('deactivate-ingredient')

    })

}

function clearCheckbox(context) {
    context.find('.constructor-popup__checkbox-item').removeClass('constructor-popup__checkbox-item--active')
    context.find('.constructor-popup__checkbox-item').removeClass('deactivate-ingredient')
}

$(document).on('click','.product-list__constructor',function(e){
    e.preventDefault();
    $(this).next('.constructor-popup').addClass('constructor-popup--active')
    $('body').addClass('body')
    
    replaceDesc($(this));
    findNoIngr($(this).next('.constructor-popup'))
    


    var checkboxes = $(this).next('.constructor-popup').find('.constructor-popup__checkbox-row');
    checkboxes.each(function() {
        checkMinIngred($(this))
    })

    countPrice($(this).next('.constructor-popup').find('.constructor-popup__inner'))

})


$(document).on('click','.constructor-popup__close, .constructor-popup__overflov',function(){
    $('.constructor-popup').removeClass('constructor-popup--active')
    $('body').removeClass('body')
})


$(document).on('click','.constructor-popup__radio-item',function(e){

    if ($(this).hasClass('deactivate') || $(this).hasClass('deactivate-ingredient')) {
        return;
    } else {

        $(this).closest('.constructor-popup__radio-row').find('.constructor-popup__radio-item').removeClass('constructor-popup__radio-item--active');
        $(this).addClass('constructor-popup__radio-item--active');
        
        replaceImg($(this));
        replaceDesc($(this));
        clearCheckbox($(this).closest('.constructor-popup'));
        findNoIngr($(this));
        $(this).closest('.constructor-popup__radio-row').find('.constructor-popup__radio-item').removeClass('constructor-popup__radio-item--active');
        $(this).addClass('constructor-popup__radio-item--active');

        var extra_charge = 0;
        var radio = $(this).closest('.constructor-popup').find('.constructor-popup__radio-item--active');
        radio.each(function() {
            
            if ($(this).data('extra')) {
                extra_charge += $(this).data('extra');
            }
            
        })

        

        
        var checkbox_id = $(this).closest('.constructor-popup').find('.constructor-popup__checkbox-item');

        checkbox_id.each(function() {
            var price = $(this).data('saveprice');
            if (extra_charge) {
                var res = price + extra_charge;
            } else {
                var res = price;
            }
            
            $(this).find('.constructor-popup__replace-price').text(res);
            $(this).data('price', res)
        })

        countPrice($(this).closest('.constructor-popup').find('.constructor-popup__inner'));
        

    }

    
})


$(document).on('click','.constructor-popup__checkbox-item',function(){
    if($(this).hasClass('deactivate') || $(this).hasClass('deactivate-ingredient')) {
        return
    } else {
        $(this).toggleClass('constructor-popup__checkbox-item--active');
    }

    var checkboxes = $(this).closest('.constructor-popup__checkbox-row');
    checkboxes.each(function() {
        
        checkMinIngred($(this))
    })
    

    
    findNoIngr($(this))
    countPrice($(this).closest('.constructor-popup').find('.constructor-popup__inner'));
})





$(document).on('click','.constructor__remove',function(e){
    e.preventDefault();
    
    var id = $(this).attr('data-id')
    var csrfToken = $(this).attr('data-token')
    
    data = {
        id: id, 
        csrfmiddlewaretoken: csrfToken
    }
    $.post( "/cart/remove_constructor/", data)
        .done(function( ) {      
            
            $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
            $('.cart__inner').load('/cart/ .cart__refresh', function() {});
            $('.cart__form-refresh').load('/cart/ .cart__form', function() {});
            $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
            
            updateMinDelivery()
        });
})

$(document).on('click','.plus_constructor',function(e){
    e.preventDefault();
    var id = $(this).attr('data-id')
    var csrfToken = $(this).attr('data-token')
    var url = $(this).attr('data-url')

    data = {
        id: id, 
        csrfmiddlewaretoken: csrfToken
    }
    $.post( url, data)
        .done(function( ) {
            $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
            $('.cart__inner').load('/cart/ .cart__refresh', function() {});
            $('.cart__form-refresh').load('/cart/ .cart__form', function() {});
            $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
            
            updateMinDelivery()
        })
})




$(document).on('submit', '.like-form', function (e) {

    e.preventDefault();

    var $form = $(this); // Сохраняем ссылку на форму

    var toggle_value = $form.find('.like-form__toggle').val();
    toggle_value = parseInt(toggle_value);
    

    $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
    }).done(function () {
        var count = parseInt($form.find('.like-form__count').text());
        // Используем сохраненную ссылку на форму
        if (toggle_value == 1) {
            $form.find('.like-form__toggle').val(0);
            $form.find('.like-form__btn').removeClass('like-form__btn--active');
            count -= 1;

        } else {
            $form.find('.like-form__toggle').val(1);
            $form.find('.like-form__btn').addClass('like-form__btn--active');
            count += 1;
        }

        // Обновляем значение лайка
        $form.find('.like-form__count').text(count)
        

    }).fail(function () {
        console.log('fail');
    });
})

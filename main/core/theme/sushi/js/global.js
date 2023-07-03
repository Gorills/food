

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
            ymaps.ready(init);
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
        $.get("/cart/set_delivery/1/", function() {
          refreshElements();
          $('#suggest').attr('required', 'required');
          $('#finaladress').attr('required', 'required').attr('name', 'address');
          $('#pickupInput').removeAttr('name');
          $('.cart__form-refresh-delivery').addClass('cart__form-refresh-delivery--active');
          $('.cart__pickup-row').removeClass('cart__pickup-row--active');
          $('#delivery_method').val('Доставка');
          $('.product-detail__button').addClass('btn--success');
        });
  
        
  
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
        $('.cart__inner').load('/cart/ .cart__refresh', function() {});
        $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});

        
       
        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
       
        

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

        
        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
        
        
        
        
        
      }).fail(function() {
        console.log('fail');
      });
      e.preventDefault();
    });
});

//   Удаление из корзины
$(document).on('click','.cart__remove, .product-remove a',function(e){
    e.preventDefault();
    var id = $(this).attr('data-id')
    var name = $(this).attr('data-name')
    var price = $(this).attr('data-price')
    var category = $(this).attr('data-category')
    var quantity = $(this).attr('data-quantity')

    var url = $(this).attr('href')
    $.get(url, function() {
     
        
        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
        $('.cart__inner').load('/cart/ .cart__refresh', function() {});
        $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});

        removeCart(id, name, price, category, quantity) 
        
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
    $parent.find('.product-options-popup_btn').attr('data-quantity', value);
});
$(document).on('click','.product-options-popup__plus',function(){
    var $parent = $(this).closest('.product-options-popup__inner');
    var value = $parent.find('.product-options-popup__count-inp').val();
    
    value++;
    
    $parent.find('.product-options-popup__count-inp').val(value);
    $parent.find('.product-options-popup_btn').attr('data-quantity', value);
});


// Options

$(document).ready(function() {
  // Для каждого блока с классом select-wrap на странице
  $('.select-wrap').each(function() {
        // Получаем первый элемент с классом select-wrap__item внутри текущего блока
        var firstOption = $(this).find('.select-wrap__item').first();
    
        // Получаем значение атрибута data-value первого элемента
        var optionValue = firstOption.attr('data-value');
    
        // Получаем значение атрибута data-price первого элемента
        var optionPrice = firstOption.attr('data-price');

        console.log(optionValue)
    
        // Находим элемент select-wrap__input внутри текущего блока и устанавливаем его значение и атрибуты data-id и data-price
        $(this).find('.select-wrap__input').val(optionValue);
        $(this).find('.select-wrap__input').attr('data-id', firstOption.attr('data-id')).attr('data-price', optionPrice);
        $(this).find('.select-wrap__checked').html(optionValue);
    });
});







$(document).on('click','.select-wrap__checked',function(){

    $(this).next('.select-wrap__row').toggleClass('select-wrap__row--active')
    $(this).parent('.select-wrap').toggleClass('select-wrap--active')
    
});


$(document).on('click','.select-wrap__item',function(){
    
    var totalPrice = parseFloat($('.product-detail__price').attr('data-price'));
    var oldPrice = parseFloat($('.product-detail__price-old').attr('data-price'));
    var optionsIds = '';
    var options = '';
    var quantity = parseInt($('#id_quantity').val());

    var res = $(this).attr('data-value')
    var id = $(this).attr('data-id')
    var price = $(this).attr('data-price')
    

    $(this).parent().next('.select-wrap__input').val(res)
    $(this).parent().next('.select-wrap__input').attr('data-id', id)
    $(this).parent().next('.select-wrap__input').attr('data-price', price)


    $(this).parent().prev('.select-wrap__checked').html(res)
    $('.select-wrap__row').removeClass('select-wrap__row--active')
    $('.select-wrap').removeClass('select-wrap--active')

    
    $('select option:selected').each(function() {
      var price = parseFloat($(this).attr('data-price'));
      totalPrice += price;
      oldPrice += price;
      optionsIds += $(this).attr('data-id') + ',';
      options += $(this).val().split(',')[0] + ',';
    });
    $('.select-wrap__input').each(function() {
        var price = parseFloat($(this).attr('data-price'));
        totalPrice += price;
        oldPrice += price;
        optionsIds += $(this).attr('data-id') + ',';
        options += $(this).val().split(',')[0] + ',';
      });
    
    $('input[type=checkbox]:checked').each(function() {
      var price = parseFloat($(this).attr('data-price'));
      totalPrice += price;
      oldPrice += price;
      optionsIds += $(this).attr('data-id') + ',';
      options += $(this).val().split(',')[0] + ',';
    });

    
    
    optionsIds = optionsIds.slice(0, -1);
    options = options.slice(0, -1);
    $('.product-detail__price-old').html(oldPrice + '₽');
    $('.product-detail__price').html(totalPrice + '₽');
    $('.options_btn').attr('data-price', totalPrice).attr('data-options-id', optionsIds).attr('data-options', options).attr('data-quantity', quantity);
});

$(document).ready(function() {
    var totalPrice = parseFloat($('.product-detail__price').attr('data-price'));
    var oldPrice = parseFloat($('.product-detail__price-old').attr('data-price'));
    var optionsIds = '';
    var options = '';
    var quantity = parseInt($('#id_quantity').val());
    
    $('select option:selected').each(function() {
        var price = parseFloat($(this).attr('data-price'));
        totalPrice += price;
        oldPrice += price;
        optionsIds += $(this).attr('data-id') + ',';
        options += $(this).val().split(',')[0] + ',';
    });
    $('.select-wrap__input').each(function() {
        var price = parseFloat($(this).attr('data-price'));
        totalPrice += price;
        oldPrice += price;
        optionsIds += $(this).attr('data-id') + ',';
        options += $(this).val().split(',')[0] + ',';
    });
    
    $('input[type=checkbox]:checked').each(function() {
        var price = parseFloat($(this).attr('data-price'));
        totalPrice += price;
        oldPrice += price;
        optionsIds += $(this).attr('data-id') + ',';
        options += $(this).val().split(',')[0] + ',';
    });

    
    
    optionsIds = optionsIds.slice(0, -1);
    options = options.slice(0, -1);
    
    $('.product-detail__price-old').html(oldPrice + '₽');
    $('.product-detail__price').html(totalPrice + '₽');
    $('.options_btn').attr('data-price', totalPrice).attr('data-options-id', optionsIds).attr('data-options', options).attr('data-quantity', quantity);
    
    $(document).on('change','input, select',function(){
    
      var totalPrice = parseFloat($('.product-detail__price').attr('data-price'));
      var oldPrice = parseFloat($('.product-detail__price-old').attr('data-price'));

      var optionsIds = '';
      var options = '';
      var quantity = parseInt($('#id_quantity').val());
      
      $('select option:selected').each(function() {
        var price = parseFloat($(this).attr('data-price'));
        totalPrice += price;
        oldPrice += price;
        optionsIds += $(this).attr('data-id') + ',';
        options += $(this).val().split(',')[0] + ',';
      });
      $('.select-wrap__input').each(function() {
        var price = parseFloat($(this).attr('data-price'));
        totalPrice += price;
        oldPrice += price;
        optionsIds += $(this).attr('data-id') + ',';
        options += $(this).val().split(',')[0] + ',';
    });
      $('input[type=checkbox]:checked').each(function() {
        var price = parseFloat($(this).attr('data-price'));
        totalPrice += price;
        oldPrice += price;
        optionsIds += $(this).attr('data-id') + ',';
        options += $(this).val().split(',')[0] + ',';
      });

      
      
      optionsIds = optionsIds.slice(0, -1);
      options = options.slice(0, -1);

      $('.product-detail__price-old').html(oldPrice + '₽');
      $('.product-detail__price').html(totalPrice + '₽');
      $('.options_btn').attr('data-price', totalPrice).attr('data-options-id', optionsIds).attr('data-options', options).attr('data-quantity', quantity);
    });
  });
  
  

  $('.options_btn, .product-options__btn, .product-options-popup_btn').click(function(e) {
    e.preventDefault();
    var options_id = $(this).attr('data-options-id');
    var options = $(this).attr('data-options');
    var products = $(this).attr('data-product');
    var products_name = $(this).attr('data-product-name');
    var category = $(this).attr('data-category');
    var quantity = parseInt($(this).attr('data-quantity'));
    var price = parseFloat($(this).attr('data-price'));

    var csrfToken = $(this).attr('data-csrf');

    console.log(options_id, options, products, quantity, price);
    addCart(products, products_name, price, category, quantity)

    var parent_get = $(this).closest('.product-options-popup');
    var btn_get = parent_get.find('.product-options-popup_btn')

    if (options && options_id && products && quantity && price) { 
        data = {
            options_id: options_id, 
            options: options,
            products: products,
            quantity:quantity, 
            price:price,
            csrfmiddlewaretoken: csrfToken
        }
    
        $.post( "/cart/add_options/", data)
        .done(function( ) {
        

            $('.options_btn').removeClass('btn--primary')
            $('.options_btn').html('Добавлен')
            $('.options_btn').addClass('btn--success')
            $('#headerCart').load('/cart/ .header__cart-wrap', function() {});

            btn_get.html('Добавлен')
            
            $('.product-options-popup').removeClass('product-options-popup--active')

            
            function explode(){


                $('.options_btn').addClass('btn--primary')
                $('.options_btn').html('В корзину')
                $('.options_btn').removeClass('btn--success')


                btn_get.html('В корзину')
               
            }
            setTimeout(explode, 1000);
    
            
        });
    } else {

        data = {
            csrfmiddlewaretoken: csrfToken,
            
            quantity:quantity
        }

        $.post( "/cart/add/"+products+'/', data)
        .done(function( ) {
        
            
            
        
         
            $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
        
            $('.product-options-popup').removeClass('product-options-popup--active')
            
            btn_get.html('Добавлен')
            function explode() {


                btn_get.html('В корзину')

               
            }
            setTimeout(explode, 1000);
            
        });

    }
    

  });
  

  $(document).on('click','.options_remove',function(e){
    e.preventDefault();
    var csrfToken = $(this).attr('data-token')
   
    var id = $(this).attr('data-id')
    
    
    data = {
        id: id, 
        csrfmiddlewaretoken: csrfToken
    }
    $.post( "/cart/remove_options/", data)
        .done(function( ) {      
            $('.cart__inner').load('/cart/ .cart__refresh', function() {});
            $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
            $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
           
            
        });
})


$(document).on('click','.plus_options',function(e){
    e.preventDefault();
    var csrfToken = $(this).attr('data-token')
    var id = $(this).attr('data-id')
    var url = $(this).attr('data-url')
    
    data = {
        id: id, 
        csrfmiddlewaretoken: csrfToken
    }
    $.post( url, data)
        .done(function( ) {      
            
            $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
            $('.cart__inner').load('/cart/ .cart__refresh', function() {});
            $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
        });
})



$(document).on('click','.product-options__item',function(e){
    var id = $(this).attr('data-id')
    var price = parseFloat($(this).attr('data-price'))
    var value = $(this).attr('data-value')
    var product_id = $(this).attr('data-product-id')
    var image = $(this).attr('data-image')
    var weight = $(this).attr('data-weight')
    var $productItem = $(this).closest('.product-list__item');

    if (weight != '') {
        $productItem.find('.product-list__weight-'+product_id).html(weight)

    }

    if (image != '') {
      
        $productItem.find('.product-list__thumb-'+product_id).attr('src', image)

    }

    var pr_price = parseFloat($('.price-'+product_id).attr('data-price'))
    var old_price = parseFloat($('.old_price-'+product_id).attr('data-price'))

    
    
    $(this).parent().find('.product-options__item').removeClass('product-options__item--active')

   
    $(this).addClass('product-options__item--active')

    

    var res_price = price + pr_price;
    var res_old_price = old_price + price;

    $productItem.find('.product-options__btn').attr('data-price', res_price).attr('data-options', value).attr('data-options-id', id)

    $productItem.find('.product-list__price').html(res_price + ' ₽')
    $productItem.find('.product-list__old').html(res_old_price + ' ₽')
    
    
    // $productItem.find('.product-options__span-'+product_id).html(value)

});



// Дополнительные опции
$(document).ready(function() {
    $('input[type="checkbox"]').change(function() {
        
            
        // Найти родительский элемент всех выбранных checkbox
        var $parent = $(this).parents('.product-options-popup__inner');
        
        // Обновить сумму всех выбранных чекбоксов
        var sum = 0;
        $parent.find('input[type="checkbox"]:checked').each(function() {
            sum += parseFloat($(this).data('price'));
        });
        var price = $parent.find('.product-options-popup__price').attr('data-price');
        var old_price = $parent.find('.product-options-popup__old-price').attr('data-price');
        var new_price = parseFloat(price) + sum;
        var new_old_price = parseFloat(old_price) + sum;

        
        // Записать новую цену в атрибут data-price кнопки .btn
        $parent.find('.btn').attr('data-price', new_price.toFixed(2));
        $parent.find('.product-options-popup__price').html(new_price + ' ₽');
        $parent.find('.product-options-popup__old-price').html(new_old_price + ' ₽');
        
        // Собрать значения data-id всех выбранных чекбоксов через запятую
        var ids = [];
        $parent.find('input[type="checkbox"]:checked').each(function() {
            ids.push($(this).data('id'));
        });
        
        // Записать значения data-id через запятую в атрибут data-options-id кнопки .btn
        $parent.find('.btn').attr('data-options-id', ids.join(','));
        
        // Собрать названия выбранных значений через запятую
        var options = [];
        $parent.find('input[type="checkbox"]:checked').each(function() {
            options.push($(this).val());
        });
        
        // Записать названия выбранных значений через запятую в атрибут data-options кнопки .btn
        $parent.find('.btn').attr('data-options', options.join(', '));
    });
  });
  

$(document).on('click','.option_setup',function(e){
    e.preventDefault();
    var $parent = $(this).parents('.product-list__item');

    var popup = $parent.find('.product-options-popup');
    popup.toggleClass('product-options-popup--active')
})


$(document).on('click','.product-options-popup__closer, .product-options-popup__layout',function(e){
    e.preventDefault();
    $(this).parents('.product-options-popup').removeClass('product-options-popup--active')
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
            ymaps.ready(init);
            
    
        });

        $('body').addClass('body')
        $.get( "/cart/set_delivery/1/", function() {});
    })

    $(document).on('click','.cart__close, .cart__closer, #cancel',function(e){
        e.preventDefault()

        $('#cartData').html('')

        $.get( "/cart/set_delivery/1/", function() {});
        $('body').removeClass('body')
    })

    $(document).on('click','.cart__order',function(e){
        e.preventDefault()
        $('.cart__form').show()
        $('#map').show()
        loadCartData() 
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

    $.get( url, function() {
        loadCartData()
        
    });

})


// Карты




var deliveryArea;
var myMap;
ymaps.ready(init);

function init() {

    var city = $('#suggest').attr('data-city')
    var zones = $('#suggest').attr('data-zones')
    var csrf = $('#suggest').attr('data-csrf')
    var flickerAPI = $('#suggest').attr('data-file-zones');
    
    var suggestView=new ymaps.SuggestView(
        'suggest', {
            provider: {
            suggest: (function(request, options) {
    
                return ymaps.suggest(request, {
                    boundedBy: myMap.getBounds()
                  });

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
                                    var deliveryPrice = item.properties._data.balloonContentBody
                                    var deliveryFree = item.properties._data.balloonContentFooter
                                    var sd=parseInt(deliveryPrice.match(/\d+/)[0]);
                                    var fd=parseInt(deliveryFree.match(/\d+/)[0]);

                                    data = {
                                        price: sd,
                                        free: fd,
                                        csrfmiddlewaretoken: csrf,
                                    }                                    

                                    $.post('/cart/delivery_summ/', data)
                                    .done(function( ) {      

                                        $('#headerCart').load('/cart/ .header__cart-wrap', function() {});


                                        

                                        $('.cart__inner').load('/cart/ .cart__refresh', function() {});
                                        $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
                                        $('.cart__deliv-method-wrap').load('/cart/ .cart__deliv-method', function() {});
                                        $('.cart-detail-wrap').load('/cart/ .cart-detail-wrap__refresh', function() {});
                                        
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


jQuery(document).ready(function () {
    var pathname = window.location.href; 
    var origin   = window.location.origin;
    var order = $('.odred-done').attr('data-order')

    
    res = pathname.replace(origin, '')
    

    if(res.indexOf('/?order=True') > -1) {
        $('.odred-done').show()
        
        // Преобразуем объект в строку JSON-формата
        var jsonString = JSON.stringify(order);

        // Заменяем символы в строке
        jsonString = jsonString.replace(/'/g, '"'); 
        var newStr = jsonString.slice(1, -1);


        // Преобразуем строку JSON-формата обратно в объект
        var newObj = JSON.parse(newStr);

       
        dataLayer.push(newObj)
        
        
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




// .combo

$(document).on('click','.open-combo',function(e){
    e.preventDefault();
    $(this).prev().prev().prev('.combo-popup').addClass('combo-popup--active')

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
      var res = itemSumm*quantity + '₽';
      comboPopup.find('.combo-popup__summ').text(res);
      comboPopup.find('.combo-popup__btn').attr('data-price', itemSumm*quantity + ',00');
      comboPopup.find('.combo-popup__summ').attr('data-final', itemSumm);
      if (dataCheck == count) {
        comboPopup.find('.combo-popup__btn').addClass('combo-popup__btn--active');
      }
    });
  
    $('.counter__btn').on('click', function(e) {
      e.preventDefault();
      var input = $(this).siblings('.counter__input');
      var currentValue = parseInt(input.val());
      if ($(this).hasClass('counter__btn--minus')) {
        if (currentValue > 1) { // Minimum value of 1
          input.val(currentValue - 1);
        }
      } else {
        input.val(currentValue + 1);
      }
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
      var res = itemSumm*quantity + ',00₽';

      comboPopup.find('.combo-popup__summ').text(res);
      comboPopup.find('.combo-popup__summ').attr('data-final', itemSumm);
      if (dataCheck == count) {
        comboPopup.find('.combo-popup__btn').addClass('combo-popup__btn--active');
      }
    });
  });





  $(document).on('click','.combo-popup__btn',function(e){
    e.preventDefault();
   

    var csrfToken = $(this).attr('data-token')
    var combo = $(this).attr('data-id')
    var comboPopup = $(this).closest('.combo-popup');
    var price = comboPopup.find('.combo-popup__summ').attr('data-final');
    var quantity = comboPopup.find('.counter__input').val();
    var name = $(this).attr('data-name');
    

    

    var dataCheck = 0;
    var count = 0;
    var comboPopup = $(this).closest('.combo-popup');
    var products = ''
    comboPopup.find('.combo-popup__parent_list').each(function() {
    if($(this).attr('data-check') != '') {
            dataCheck ++;
            
        } 
        count++;

        
        products += $(this).attr('data-check') + ','
    
 
    });

    data = {
        combo: combo, 
        price:price,
        quantity:quantity,
        products: products,
        csrfmiddlewaretoken: csrfToken
    }

    if (dataCheck == count) {
        // console.log(data)
        $.post( "/cart/add_combo/", data)
            .done(function( ) {
            
                comboPopup.removeClass('combo-popup--active');
                
                $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
            


                addCart(combo, name, price, 'Комбо', quantity)
            });
    }
})


$(document).on('click','.combo__remove',function(e){
    e.preventDefault();
    var csrfToken = $(this).attr('data-token')
    var combo = $(this).attr('data-id')
    var id = $(this).attr('data-meta')
    var name = $(this).attr('data-name')
    var price = $(this).attr('data-price')
    var quantity = $(this).attr('data-quantity')
    data = {
        combo: combo, 
        csrfmiddlewaretoken: csrfToken
    }
    $.post( "/cart/remove_combo/", data)
        .done(function( ) {      
            
            $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
            $('.cart__inner').load('/cart/ .cart__refresh', function() {});
            $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
            removeCart(id, name, price, 'Комбо', quantity)
        });
})


$(document).on('click','.plus_combo',function(e){
    e.preventDefault();
    var csrfToken = $(this).attr('data-token')
    var combo = $(this).attr('data-id')
    var url = $(this).attr('data-url')
    var id = $(this).attr('data-meta')
    var name = $(this).attr('data-name')
    var price = $(this).attr('data-price')
    data = {
        combo: combo, 
        csrfmiddlewaretoken: csrfToken
    }
    $.post( url, data)
        .done(function( ) {      
            
            $('#headerCart').load('/cart/ .header__cart-wrap', function() {});
            $('.cart__inner').load('/cart/ .cart__refresh', function() {});
            $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
            
            if (url.indexOf('plus_combo') > -1) {
                addCart(combo, name, price, 'Комбо', 1)
            } else if (url.indexOf('minus_combo') > -1) {
                removeCart(id, name, price, 'Комбо', 1)
            }
        });
})
  




// header__subdomain-check

$(document).on('click','.header__subdomain-check',function(e){
    e.preventDefault();
    $('.header__subdomain-drop').toggleClass('header__subdomain-drop--active');
})

$(document).on('click','.content',function(){
   
    $('.header__subdomain-drop').removeClass('header__subdomain-drop--active');
})







  

  $(document).ready(function() {
    var isHidden = getCookie('isHidden');
  
    if (isHidden === 'true') {
      $('.delivery-popup').hide();
      $('.delivery-popup__btn').prop('disabled', true);
    } else {
        $('.delivery-popup').addClass('delivery-popup--active');
        
    }
  
    $('.delivery-popup__btn').click(function() {
      $('.delivery-popup').hide();
      $(this).prop('disabled', true);
  
      setCookie('isHidden', 'true', 1/24); // Устанавливаем куку на 1 день (время указано в днях)
    });
  });
  
  // Функция для установки куки
  function setCookie(name, value, days) {
    var expires = '';
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = '; expires=' + date.toUTCString();
    }
    document.cookie = name + '=' + (value || '') + expires + '; path=/';
  }
  
  // Функция для получения значения куки по имени
  function getCookie(name) {
    var nameEQ = name + '=';
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) === ' ') {
        c = c.substring(1, c.length);
      }
      if (c.indexOf(nameEQ) === 0) {
        return c.substring(nameEQ.length, c.length);
      }
    }
    return null;
  }
  
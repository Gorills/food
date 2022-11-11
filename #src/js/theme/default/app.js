
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

// Корзина

$(document).on('click','.header__cart',function(e){
    e.preventDefault()
    $('.cart').addClass('cart--active')
})
$(document).on('click','.cart__close, .cart__closer',function(e){
    e.preventDefault()
    $('.cart').removeClass('cart--active')
})


// Добавление в корзину product-list__form
$(function() {
    $(document).on('submit','.product-list__form, .product-detail__form, .qtybutton',function(e){
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
    if(height > 350){
        $('.header').addClass('header--hide');
        
        
    } else{
        /*Если меньше 100px удаляем класс для header*/
        $('.header').removeClass('header--hide');
              
    }
    if(height > 450){
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


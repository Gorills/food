
// Функции математики в корзине


// Сумма всех скидок
function getAllDiscount() {

    var discountOnPickup = JSON.parse(localStorage.getItem('shopSettings')).discount_on_pickup;
    var deliveryType = localStorage.getItem("deliveryType"); 
    
    var pickup_discount_summ = 0
    if (deliveryType == '0') {

        pickup_discount_summ = getTotalPrice() * discountOnPickup / 100
        // document.getElementById("discountOnPickup").innerText = `${pickup_discount_summ} - ${discountOnPickup}%`;

    } else {
        // document.getElementById("discountOnPickup").innerText = '';
    }



    return pickup_discount_summ



}


// Сумма заказа без доставки и скидок
function getTotalPrice() {
    
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    let totalPrice = 0;

    for (let itemId in cart) {
        let item = cart[itemId];
        

        totalPrice += item.price * item.quantity;
        
    }
    document.getElementById("total_price").innerText = totalPrice;
    return totalPrice
}



// Общая сумма с доставкой и скидками
function getTotalPriceAfterDiscount() {

    var discountOnPickup = JSON.parse(localStorage.getItem('shopSettings')).discount_on_pickup; 


    res = getTotalPrice() + getDeliverySumm() - getAllDiscount()

    

    return res
}






// Возвращаем финальную стоимость доставки с учетом способа доставки и условий
function getDeliverySumm() {
    let delivery = JSON.parse(localStorage.getItem('deliveryPrice'));
    

    if (delivery.free_delivery > getTotalPrice()) {
        var summ = delivery.price_delivery
    } else {
        var summ = 0
    }

    var deliveryType = localStorage.getItem("deliveryType");

    

    
    if (deliveryType === "0") {
        summ = 0
    }
    


    // document.getElementById("total_delivery").innerText = summ;
    return summ

}


// Количество товаров в корзине
function getTotalCount() {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    var totalCount = 0

    for (let itemId in cart) {
        let item = cart[itemId];
        

        totalCount += item.quantity;
        
    }

    return totalCount

}

// console.log(getDeliverySumm())


function updateAll() {
    displayCart();
    getDeliverySumm();
    getTotalPrice();
    getTotalPriceAfterDiscount();
    getTotalCount();

}





$(document).on('click','.cart__btn',function(e){
    e.preventDefault();
    $('.cart').addClass('cart--active')
    $('body').addClass('body')
    
})

$(document).on('click','.cart__owerlay, .cart__closer',function(e){
    e.preventDefault()

    $('.cart').removeClass('cart--active');
    
  

    // $.get( "/cart/set_delivery/1/", function() {});
    $('body').removeClass('body')
})

$(document).on('submit','.save-delivery',function(e){
  e.preventDefault();
  updateDeliveryType()
})

$(document).on('click','.check-delivery__item--delivery',function(e){
  e.preventDefault();
  document.getElementById("setup-address").style.display = 'flex';
})

$(document).on('click','.setup-address__close, .setup-address__overlay',function(){
    document.getElementById("setup-address").style.display = 'none';

})


document.addEventListener('click', function(event) {
    var target = event.target;
    var setupAddress = document.getElementById("set_delivery");
    if (target === setupAddress) {
        document.getElementById("check-delivery").style.display = 'flex';
    }
});

// Проверяем наличие типа доставки в localStorage
function updateDeliveryType() {
  var deliveryType = localStorage.getItem("deliveryType");
//   console.log(deliveryType)
  if (deliveryType) {
      document.getElementById("check-delivery").style.display = 'none';
      document.getElementById("setup-address").style.display = 'none';
  } else {
      document.getElementById("check-delivery").style.display = 'flex';
      
  }
  retrieveFromLocalStorage()
}
updateDeliveryType()

    
function saveToLocalStorage(deliveryType) {
  localStorage.setItem("deliveryType", deliveryType);
  retrieveFromLocalStorage();
  updateAll()
}

function retrieveFromLocalStorage() {
  var retrievedDeliveryType = localStorage.getItem("deliveryType");
  if (retrievedDeliveryType !== null) {
    var deliveryTypeText = (retrievedDeliveryType === "1") ? "1" : "0";
    document.getElementById("output").innerText = deliveryTypeText;
  } else {
    document.getElementById("output").innerText = "Тип доставки не выбран.";
  }
}





function deliveryUpdate(deliveryPriceJson) {
//   document.getElementById("price_delivery").innerText = deliveryPriceJson.price_delivery;
//   document.getElementById("free_delivery").innerText = deliveryPriceJson.free_delivery;
//   document.getElementById("min_delivery").innerText = deliveryPriceJson.min_delivery;
//   document.getElementById("first_delivery").innerText = deliveryPriceJson.first_delivery;
//   document.getElementById("delivery_address").innerText = deliveryPriceJson.delivery_address;
}


// Инициализируем стоимость доставки при первой загрузке
function setDeliveryPrice() {

    var storedSettingsJson = JSON.parse(localStorage.getItem('shopSettings'));

    var deliveryPrice = localStorage.getItem('deliveryPrice');

    var zones_delivery = storedSettingsJson.zones_delivery;
    
    var data_get = JSON.parse(deliveryPrice);

    var data = {
        'price_delivery': 0,
        'free_delivery': 0,
        'min_delivery': 0,
        'first_delivery': 0,
        'delivery_address': ''
    }

    if (!zones_delivery) {
        data = {
            'price_delivery': storedSettingsJson.price_delivery,
            'free_delivery': storedSettingsJson.free_delivery,
            'min_delivery': storedSettingsJson.min_delivery,
            'first_delivery': storedSettingsJson.first_delivery,
            'delivery_address': ''
        } 
    } 

    if (deliveryPrice) {
        

        if (JSON.stringify(data_get) !== JSON.stringify(data) && !zones_delivery) {
        // Если данные изменились на сервере, обновляем их в localStorage
        localStorage.setItem('deliveryPrice', JSON.stringify(data));
        }

    } else {
        localStorage.setItem('deliveryPrice', JSON.stringify(data));
        
    }

    
}







  function fetchAndSaveSettings() {
    fetch('/api/v1/get_shop_settings/')
        .then(response => response.json())
        .then(data => {

            // Прогружаем общие нстройки
            var storedSettings = localStorage.getItem('shopSettings');
            if (storedSettings) {
                var storedData = JSON.parse(storedSettings);
                if (JSON.stringify(storedData) !== JSON.stringify(data)) {
                    // Если данные изменились на сервере, обновляем их в localStorage
                    localStorage.setItem('shopSettings', JSON.stringify(data));
                }
            } else {
                // Если данных в localStorage нет, сохраняем их
                localStorage.setItem('shopSettings', JSON.stringify(data));
            }
            var storedSettingsJson = JSON.parse(localStorage.getItem('shopSettings'));


            // console.log(storedSettingsJson)


            // Вот тут пишем нужный код после обработки загрузки настроек.
            
            setDeliveryPrice()

            
            
              
            var deliveryPriceJson = JSON.parse(localStorage.getItem('deliveryPrice'));
            deliveryUpdate(deliveryPriceJson)


            updateAll()

            // Подключаем загрузку всех данных в HTML



        })
        .catch(error => console.error('Ошибка загрузки настроек:', error));
  }
  
  fetchAndSaveSettings();








//   Товары
// Функция для добавления товара в корзину
async function getProductOptionsId(itemId, optionsIdArray) {
    
    try {
        const response = await fetch(`/api/v1/products/${itemId}/`);
        const data = await response.json();

        return data.options.filter(option => optionsIdArray.includes(option.id));

    } catch (error) {
        console.error('Ошибка загрузки настроек:', error);
        throw error;
    }
}
async function addToCart(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    let itemElement = document.querySelector(`[data-cart-id="${itemId}"]`);
    let optionsIdString = itemElement.dataset.optionsid;
    let optionsIdArray = optionsIdString.split(",").filter(optionId => optionId.trim() !== "").map(optionId => parseInt(optionId.trim(), 10));


    let id = itemId;
    
    var optionsNameArray = [];
    if (optionsIdArray.length > 0) {
        id += optionsIdArray.join('');
        
        if (itemElement.dataset.type === 'product') {
            try {
                optionsNameArray = await getProductOptionsId(itemId, optionsIdArray);
                

            } catch (error) {
                console.error('Ошибка при получении настроек продукта:', error);
                // Возможно, здесь нужно предпринять какие-то действия при возникновении ошибки
            }
        }
    }
    
    console.log(id)
    let itemInfo = {
        id: id,
        type: itemElement.dataset.type,
        name: itemElement.dataset.name,
        price: parseFloat(itemElement.dataset.price),
        image: itemElement.dataset.image,
        quantity: cart[id] ? cart[id].quantity + 1 : 1,
        options: optionsIdArray,
        options_name: optionsNameArray
    };

    cart[id] = itemInfo;
    localStorage.setItem('cart', JSON.stringify(cart));
    
    updateAll();
}






// Функция для отображения содержимого корзины
function displayCart() {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    let cartItems = document.getElementById('cart-items');
    
    
    let totalCount = getTotalCount()

    cartItems.innerHTML = '';

    if (totalCount === 0) {
        cartItems.innerHTML = `
            <div class="cart__empty">

                <svg width="276" height="276" viewBox="0 0 276 276" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
                    <rect width="276" height="276" fill="url(#pattern0)"/>
                    <defs>
                    <pattern id="pattern0" patternContentUnits="objectBoundingBox" width="1" height="1">
                    <use xlink:href="#image0_77_2" transform="scale(0.00195312)"/>
                    </pattern>
                    <image id="image0_77_2" width="512" height="512" xlink:href="data:image/png;base64,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"/>
                    </defs>
                </svg>
            
                <p>Ваша корзина пока пуста</p>
                
            </div>
        
        `;
        cartItems.style.height = 'fit-content;';
        document.getElementById('cart-bottom').style.display = 'none';
    } else {

        
        for (let itemId in cart) {
            let item = cart[itemId];
            let cartItem = document.createElement('li');


            let options_name = item.options_name

            let options_str = ''

            if (options_name) {

                for (const item of options_name) {

                    options_str += `<div class="cart__item-option">${item.option_value}</div>`
                }
            }
                
            

            cartItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}" style="width: 100px;">

                <div class="cart__item-info">

                    <span class="cart__item-name">${item.name}</span>

                    <div class="cart__item-options">${options_str}</div>

                </div>
                <div class="cart__btn-wrapper">
                    <button class="cart__plusminus" onclick="minusFromCart(${itemId})">-</button>
                    <div class class="cart__quantity">${item.quantity}</div>
                    <button class="cart__plusminus" onclick="plusFromCart(${itemId})">+</button>
                </div>

                <div class="cart__summ">${item.price * item.quantity} ₽</div>
                <button class="cart__remove" onclick="removeFromCart(${itemId})">
                    
                    <?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                    <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20.5001 6H3.5" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                    <path d="M9.5 11L10 16" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                    <path d="M14.5 11L14 16" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                    <path d="M6.5 6C6.55588 6 6.58382 6 6.60915 5.99936C7.43259 5.97849 8.15902 5.45491 8.43922 4.68032C8.44784 4.65649 8.45667 4.62999 8.47434 4.57697L8.57143 4.28571C8.65431 4.03708 8.69575 3.91276 8.75071 3.8072C8.97001 3.38607 9.37574 3.09364 9.84461 3.01877C9.96213 3 10.0932 3 10.3553 3H13.6447C13.9068 3 14.0379 3 14.1554 3.01877C14.6243 3.09364 15.03 3.38607 15.2493 3.8072C15.3043 3.91276 15.3457 4.03708 15.4286 4.28571L15.5257 4.57697C15.5433 4.62992 15.5522 4.65651 15.5608 4.68032C15.841 5.45491 16.5674 5.97849 17.3909 5.99936C17.4162 6 17.4441 6 17.5 6" stroke="#1C274C" stroke-width="1.5"/>
                    <path d="M18.3735 15.3991C18.1965 18.054 18.108 19.3815 17.243 20.1907C16.378 21 15.0476 21 12.3868 21H11.6134C8.9526 21 7.6222 21 6.75719 20.1907C5.89218 19.3815 5.80368 18.054 5.62669 15.3991L5.16675 8.5M18.8334 8.5L18.6334 11.5" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                    </svg>
                </button>
            `;
            
            cartItems.appendChild(cartItem);
            document.getElementById('cart-bottom').style.display = 'block';
            
            
        }
    }
    

    // Отображаем общую стоимость и количество товаров
    let totalInfo = document.createElement('li');

    document.getElementById("cart_summ").innerText = getTotalPrice();
    document.getElementById("cart_num").innerText = totalCount;

    // totalInfo.textContent = `Общая стоимость: ${getTotalPrice()}`;

    cartItems.appendChild(totalInfo);

    
    setDeliveryPrice()
}


function minusFromCart(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    if (cart[itemId].quantity > 1) {
        cart[itemId].quantity--;
    } else {
        delete cart[itemId];
    }
    localStorage.setItem('cart', JSON.stringify(cart));
   
    updateAll()
}

function plusFromCart(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    cart[itemId].quantity++;
    localStorage.setItem('cart', JSON.stringify(cart));
    
    updateAll()
}

// Функция для удаления товара из корзины
function removeFromCart(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    delete cart[itemId];
    localStorage.setItem('cart', JSON.stringify(cart));
   
    updateAll()
}

// Функция для очистки корзины
function clearCart() {
    localStorage.removeItem('cart');
    
    updateAll()
}
// clearCart()
// При загрузке страницы отображаем содержимое корзины, если оно есть







































var deliveryArea;
var myMap;
ymaps.ready(init);

function init() {

    var city = $('#suggest').attr('data-city')
    var zones = $('#suggest').attr('data-zones')
    var csrf = $('#suggest').attr('data-csrf')
    var flickerAPI = $('#suggest').attr('data-file-zones');
    var datathirdPartyDdelivery = $('#suggest').attr('data-third-party-delivery');

    
    
    if (zones != 'false') {
        
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

    } 

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
                        
                        if(datathirdPartyDdelivery == 'false') {
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
                        } else {
                            freeArea = new ymaps.Polygon(
                                [
                                    val.coords
                                ], {
                                    
                                }, {
                            
                                fillColor: val.fillColor,
                                strokeColor: val.strokeColor,
                                opacity: val.opacity
                            });
                            myMap.geoObjects.add(freeArea);
                            count+=1

                        }

                        
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

                                    var suggestElement = $('#suggest');
                                    var headerCartElement = $('#headerCart');
                                    var cartInnerElement = $('.cart__inner');

                                    
                                    if (datathirdPartyDdelivery == 'true') {
                                        
                                        data_del = {
                                            
                                            dotaddress: suggestElement.val(),
                                            csrfmiddlewaretoken: csrf
                                        }

                                        $.post("/delivery/check_price/", data_del, function(response) {
                                            // Парсинг JSON-ответа
                                            var price = response.price;
                                            
                                            console.log(price);
                                            
                                            $('#suggest').attr('data-delivery', price)
                                            $('#suggest').attr('data-free', 0)
                                            $('#suggest').attr('data-value', suggestElement.val())
                                            $('#suggest').attr('data-min', 0)
                                        
                                        });
                                        

                                    } else {

                                        var deliveryText = item.properties._data.hintContent
                                        var deliveryPrice = item.properties._data.balloonContentBody
                                        var deliveryFree = item.properties._data.balloonContentFooter
                                        var sd=parseInt(deliveryPrice.match(/\d+/)[0]);
                                        var fd=parseInt(deliveryFree.match(/\d+/)[0]);
                                        var min_delivery = item.properties._data.balloonContentFooter.match(/\d+/g)[1];
    
                                        

                                        var data = JSON.parse(localStorage.getItem('deliveryPrice'));

                                        data.price_delivery = sd
                                        data.free_delivery = fd
                                        data.delivery_address = suggestElement.val()
    
                                        if(min_delivery) {
                                            var min_delivery_post = parseInt(item.properties._data.balloonContentFooter.match(/\d+/g)[1]);

                                            data.min_delivery = min_delivery_post
                                            $('#suggest').attr('data-min', min_delivery_post)
                                        } 

                                        localStorage.setItem('deliveryPrice', JSON.stringify(data));


                                        var deliveryPriceJson = JSON.parse(localStorage.getItem('deliveryPrice'));
                                        deliveryUpdate(deliveryPriceJson)

                                    }
                                    
                                    

    
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
                                    
                                    myMap.geoObjects.removeAll()
                                    getzones()
                                    myMap.geoObjects.add(item)
                                    myMap.geoObjects.add(myGeoObject)
                                    myMap.setCenter(obj.geometry._coordinates);
                                    myMap.setZoom(17);



                                 
                                    

                                    

                                    suggestElement.removeClass('suggest-error')
                                    $('#addressError').text('')
                                    $('#addressError').hide()
                                    $('#finaladress').val($('#suggest').val())
                                    suggestElement.css('border-color', 'green');
                                    suggestElement.attr('data-value', $('#suggest').val());


                                    
                                    
                                    
    
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
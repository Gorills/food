
// Функции математики в корзине


// Сумма всех скидок
function getAllDiscount() {

    var discountOnPickup = JSON.parse(localStorage.getItem('shopSettings')).discount_on_pickup;
    var deliveryType = localStorage.getItem("deliveryType"); 
    
    var pickup_discount_summ = 0
    if (deliveryType == '0') {

        pickup_discount_summ = getTotalPrice() * discountOnPickup / 100
        document.getElementById("discountOnPickup").innerText = `${pickup_discount_summ} - ${discountOnPickup}%`;

    } else {
        document.getElementById("discountOnPickup").innerText = '';
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

    return totalPrice
}



// Общая сумма с доставкой и скидками
function getTotalPriceAfterDiscount() {

    var discountOnPickup = JSON.parse(localStorage.getItem('shopSettings')).discount_on_pickup; 


    res = getTotalPrice() + getDeliverySumm() - getAllDiscount()

    document.getElementById("total_price").innerText = res;

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
    


    document.getElementById("total_delivery").innerText = summ;
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
  console.log(deliveryType)
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
  document.getElementById("price_delivery").innerText = deliveryPriceJson.price_delivery;
  document.getElementById("free_delivery").innerText = deliveryPriceJson.free_delivery;
  document.getElementById("min_delivery").innerText = deliveryPriceJson.min_delivery;
  document.getElementById("first_delivery").innerText = deliveryPriceJson.first_delivery;
  document.getElementById("delivery_address").innerText = deliveryPriceJson.delivery_address;
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
function addToCart(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    let dataType = document.querySelector(`[data-cart-id="${itemId}"]`);    
    console.log(dataType)

    let itemInfo = {
        id: itemId,
        type: document.querySelector(`[data-cart-id="${itemId}"]`).dataset.type,
        name: document.querySelector(`[data-cart-id="${itemId}"]`).dataset.name,
        price: parseFloat(document.querySelector(`[data-cart-id="${itemId}"]`).dataset.price),
        image: document.querySelector(`[data-cart-id="${itemId}"]`).dataset.image,
        quantity: cart[itemId] ? cart[itemId].quantity + 1 : 1,
        options: {}
    };

    cart[itemId] = itemInfo;
    localStorage.setItem('cart', JSON.stringify(cart));
    console.log(cart)
    
    updateAll()
}






// Функция для отображения содержимого корзины
function displayCart() {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    let cartItems = document.getElementById('cart-items');
    
    
    let totalCount = getTotalCount()

    cartItems.innerHTML = '';

    if (totalCount === 0) {
        cartItems.innerHTML = 'Корзина пуста';
    } else {
        for (let itemId in cart) {
            let item = cart[itemId];
            let cartItem = document.createElement('li');
            cartItem.innerHTML = `
                <img src="${item.image}" alt="${item.name}" style="width: 50px;">
                <span>${item.name} - ${item.price} x ${item.quantity}</span>
                <button onclick="minusFromCart(${itemId})">-</button>
                <button onclick="plusFromCart(${itemId})">+</button>
                <button onclick="removeFromCart(${itemId})">Удалить</button>
            `;
            cartItems.appendChild(cartItem);
    
            
            
        }
    }
    

    // Отображаем общую стоимость и количество товаров
    let totalInfo = document.createElement('li');

    document.getElementById("cart_summ").innerText = getTotalPrice();
    document.getElementById("cart_num").innerText = totalCount;

    totalInfo.textContent = `Общая стоимость: ${getTotalPrice()}`;

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
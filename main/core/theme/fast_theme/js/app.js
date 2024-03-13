
$(document).on('submit','.save-delivery',function(e){
  e.preventDefault();
  updateDeliveryType()
})

$(document).on('click','.check-delivery__item--delivery',function(e){
  e.preventDefault();
  document.getElementById("setup-address").style.display = 'flex';
})


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
}


// Инициализируем стоимость доставки при первой загрузке
function setDeliveryPrice(storedSettingsJson) {

  var deliveryPrice = localStorage.getItem('deliveryPrice');

  var zones_delivery = storedSettingsJson.zones_delivery;
  
  var data_get = JSON.parse(deliveryPrice);

  var data = {
    'price_delivery': 0,
    'free_delivery': 0,
    'min_delivery': 0,
    'first_delivery': 0
  }

  if (!zones_delivery) {
    data = {
        'price_delivery': storedSettingsJson.price_delivery,
        'free_delivery': storedSettingsJson.free_delivery,
        'min_delivery': storedSettingsJson.min_delivery,
        'first_delivery': storedSettingsJson.first_delivery
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


            // Вот тут пишем нужный код после обработки загрузки настроек.
            
            setDeliveryPrice(storedSettingsJson)

            
            
              
            var deliveryPriceJson = JSON.parse(localStorage.getItem('deliveryPrice'));
            deliveryUpdate(deliveryPriceJson)

            // Подключаем загрузку всех данных в HTML



        })
        .catch(error => console.error('Ошибка загрузки настроек:', error));
  }
  
  fetchAndSaveSettings();














































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
    
                                        

                                        
                                        $('#suggest').attr('data-delivery', sd)
                                        $('#suggest').attr('data-free', fd)
                                        $('#suggest').attr('data-value', suggestElement.val())

                                        var data = JSON.parse(localStorage.getItem('deliveryPrice'));

                                        data.price_delivery = sd
                                        data.free_delivery = fd
    
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



                                    headerCartElement.load('/cart/ .header__cart-wrap', function() {});
                                    cartInnerElement.load('/cart/ .cart__refresh', function() {});
                                    $('.cart__order-create-wrapper').load('/cart/ .cart__order-create-wrapper-inner', function() {});
                                    $('.cart__deliv-method-wrap').load('/cart/ .cart__deliv-method', function() {});
                                    $('.cart-detail-wrap').load('/cart/ .cart-detail-wrap__refresh', function() {});
                                    $('.cart__form-delivery-in-session').load('/cart/ .cart__form-delivery-in-session-ref', function() {});
                                    

                                    

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
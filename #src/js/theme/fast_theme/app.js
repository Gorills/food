


// Сначала загружаем все настройки

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
            setPickupPoints()
            
            
            deliveryUpdate()
            deliveryTimeUpdate();
            getDeliverySumm()


            updateAll()
            
            // Подключаем загрузку всех данных в HTML



        })
        .catch(error => console.error('Ошибка загрузки настроек:', error));
}
  
fetchAndSaveSettings();



function setLoyalCart() {
    
    let data = {
        'cart_balls': 0,
        'percent_down': 0,
        'percent_down_pickup': 0,
        'percent_pay': 0,
        'percent_pay_pickup': 0,
        'balls_min_summ': 0,
        'exclude_combos': false,
        'exclude_sales': false,
    }

    fetch('/api/v1/get_user/')
        .then(response => response.json())
        .then(data => {

            if (data.phone != 'error') {
            
                if (data.cart_status) {

                    data = {
                        'cart_balls': data.cart_balls,
                        'percent_down': data.percent_down,
                        'percent_down_pickup': data.percent_down_pickup,
                        'percent_pay': data.percent_pay,
                        'percent_pay_pickup': data.percent_pay_pickup,
                        'balls_min_summ': data.balls_min_summ,
                        'exclude_combos': data.exclude_combos,
                        'exclude_sales': data.exclude_sales,
                    }

                    localStorage.setItem('loyalCart', JSON.stringify(data));
                    
                } else {
                    data = {
                        'cart_balls': 0,
                        'percent_down': 0,
                        'percent_down_pickup': 0,
                        'percent_pay': 0,
                        'percent_pay_pickup': 0,
                        'balls_min_summ': 0,
                        'exclude_combos': false,
                        'exclude_sales': false,

                    }

                    localStorage.setItem('loyalCart', JSON.stringify(data));

                }
            } else {

                data = {
                    'cart_balls': 0,
                    'percent_down': 0,
                    'percent_down_pickup': 0,
                    'percent_pay': 0,
                    'percent_pay_pickup': 0,
                    'balls_min_summ': 0,
                    'exclude_combos': false,
                    'exclude_sales': false,
                }

                localStorage.setItem('loyalCart', JSON.stringify(data));
            }
                
                
            
        })
        .catch(error => console.error('Ошибка загрузки пользователя:', error));


    


    let loyalCart = JSON.parse(localStorage.getItem('loyalCart'));
    // console.log(loyalCart)
    
}

setLoyalCart()


// Инициализируем пустой заказ
function setOrder() {

    data = {
        'order_id': '',
        'user_id': '',
        'user_name': '',
        'user_phone': '',
        'address': '',
        'address_pickup': '',
        'address_comment': '',
        'cutlery': 0,
        'delivery_type': '',
        'entrance': '',
        'floor': '',
        'flat': '',
        'door_code': '',
        'data_time': 0,
        'day': 'Сегодня',
        'time': 'Как можно скорее',
        'pay_method': '',
        'pay_change': '',
        'delivery_method': '',
        'delivery_price': '',
        'order_conmment': '',
        'summ': '',
        'sale_percent': 0,
        'bonuses_pay': 0,
        'status': 'Новый',
        'coupon': '',
        'discount': '',
        'balls': 0,
        'percent_pay': 0,
        'delivery_status': '',
    }

    var order = localStorage.getItem('order');

    if (!order) {
        localStorage.setItem('order', JSON.stringify(data));
    }

    var order = JSON.parse(localStorage.getItem('order'));

    // console.log(order)

    
    document.getElementById('day').innerHTML = order.day;
    document.getElementById('time').innerHTML = order.time;


    // Отображаем выбранное время и настройки для доставки
    if (order.data_time == 0) {
        document.getElementById('checkout__radio-bytime').checked = false;
        document.getElementById('checkout__radio-now').checked = true;

        document.getElementById('order__times-row').style.display = 'none';

    } else {
        document.getElementById('checkout__radio-bytime').checked = true;
        document.getElementById('checkout__radio-now').checked = false;
        document.getElementById('order__times-row').style.display = 'block';

    }

    // console.log(order)

    let phone = ''
    fetch('/api/v1/get_user/')
        .then(response => response.json())
        .then(data => {
            if (data.phone != 'error') {
               

                order.user_phone = data.phone;
                localStorage.setItem('order', JSON.stringify(order));


                if (data.cart_status) {

                    
                    


                }
                
                
            }

            

            
        })
        .catch(error => console.error('Ошибка загрузки пользователя:', error));

}

setOrder()








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
      
      var order = JSON.parse(localStorage.getItem('order'));
  
      if (deliveryTypeText == '0') {
          order.delivery_method = 'Самовывоз'
          order.delivery_type == '0'
      } else {
          order.delivery_method = 'Доставка'
          order.delivery_type == '1'
      }
      
      localStorage.setItem('order', JSON.stringify(order));
  
      updateDeliveryInfo(deliveryTypeText)
    } 
  
  
  }
  
  // Обновление информации о доставке в html
  function updateDeliveryInfo(deliveryTypeText) {

    $('.order__pay-methods').hide()
    $('.order__body-wrap').show()

    $('.order .checkout__counter-item:nth-child(2)').removeClass('checkout__counter-item--active checkout__counter-item--line');
    $('.order .checkout__counter-item:nth-child(1)').removeClass('checkout__counter-item--line');

    let htmlInner = 
        `
      
        <a href="#" class="btn btn--primary order__next">Далее</a>
        `

    $('.order__next-wrap').html(htmlInner)

      if (deliveryTypeText === "1") {


          document.querySelector('.order-delivery').classList.add('order__delivery-check-item--active');
          document.querySelector('.order-pickup').classList.remove('order__delivery-check-item--active');
  
          document.getElementById("order_delivery").style.display = 'block';
          document.getElementById("order_pickup").style.display = 'none';

          $('.order__next').addClass('order__next--delivery');
          $('.order__next').removeClass('order__next--pickup');
          
          $('#total_delivery_info').show()
  
  
          let deliveryPrice = JSON.parse(localStorage.getItem('deliveryPrice'));
          let shopSetup = JSON.parse(localStorage.getItem('shopSettings'));
          let order = JSON.parse(localStorage.getItem('order'));
          // console.log(shopSetup)
  
          let street = document.getElementById("street")

          $('#street').addClass('required')
          // .attr('readonly', 'readonly')

          if (shopSetup.zones_delivery) {
              street.value = order.address;
              street.readOnly = true;
              street.style.cursor = 'pointer';
              street.classList.add('show-map');
          } else {
              street.value = order.address;
              street.readOnly = false;
              street.style.cursor = 'auto';
              
          }
         
          
  
  
      } else {
          

        $('#street').removeClass('required')
          document.querySelector('.order-delivery').classList.remove('order__delivery-check-item--active');
          document.querySelector('.order-pickup').classList.add('order__delivery-check-item--active');
  
          document.getElementById("order_delivery").style.display = 'none';
          document.getElementById("order_pickup").style.display = 'block';

          $('.order__next').removeClass('order__next--delivery');
          $('.order__next').addClass('order__next--pickup');

          $('#total_delivery_info').hide()
  
      }



  }
  
  
//   Заполнение способов оплаты
function payMethodUpdate() {
    var storedSettingsJson = JSON.parse(localStorage.getItem('shopSettings'));

    var deliveryType = localStorage.getItem("deliveryType");
    var order = JSON.parse(localStorage.getItem('order'));

    // console.log(order)

    
    var payMethods = storedSettingsJson.pay_methods.filter(function(method) {
        if (deliveryType === '0') {
            return method.in_pay_pickup === true;
        } else {
            return method.in_pay_delivery === true;
        }
    });


    var radioList = document.querySelector('.checkout__radio-list');
    radioList.innerHTML = ''; // Очистка списка
    var count = 0;
    payMethods.forEach(function(method, index) {
        var label = document.createElement('label');
        label.classList.add('checkout__radio-wrap');

        var input = document.createElement('input');
        input.type = 'radio';
        input.classList.add('checkout__radio');
        input.name = 'checkoutpayment';
        input.value = method.name;
        input.dataset.tab = 'checkout-payment-1';
        
        // Если count равен 0, устанавливаем атрибут checked для первого радио
        if (count === 0) {
            input.checked = true;
            order.pay_method = method.name;
            localStorage.setItem('order', JSON.stringify(order));

            // Проверяем, содержит ли method.name строку "наличн" в любом регистре
            if (method.name.toLowerCase().includes("наличн")) {
                // Выполняем нужное действие
                $('#pay_change').show()
                // Добавьте здесь свои действия
            } else {
                $('#pay_change').hide()
            }
        }

        var span = document.createElement('span');
        span.textContent = method.name;

        label.appendChild(input);
        label.appendChild(span);
        radioList.appendChild(label);

        count++;
    });

}


// Заполнение точек самовывоза
function setPickupPoints() {
    var storedSettingsJson = JSON.parse(localStorage.getItem('shopSettings'));

    var order = JSON.parse(localStorage.getItem('order'));

    

    var pickup_areas = storedSettingsJson.pickup_areas;
    var areaWrap = document.querySelector('.order__pickup-areas');

    // Очищаем содержимое .order__pickup-areas
    areaWrap.innerHTML = '';
    var count = 0;
    pickup_areas.forEach(function(area) {
        var label = document.createElement('label');
        label.classList.add('order__pickup-areas-item');

        var input = document.createElement('input');
        input.type = 'text';
        input.classList.add('order__input');
        input.classList.add('order__input-dropdown');
        input.name = 'pickup_point';
        input.value = area.name;
        input.readOnly = true; // добавлено readonly

        var span = document.createElement('span');
        span.textContent = area.name;

        label.appendChild(input);
        areaWrap.appendChild(label);

        if (count === 0) {
            input.classList.add('order__input');

            order.address_pickup = area.name;
            localStorage.setItem('order', JSON.stringify(order));

            document.querySelector('.order__pickup-areas-input').value = area.name;
        }

        count++;
    });

    if (count == 1) {
        var areaWrap = document.querySelector('.order__pickup-areas');
        var svgItem = document.querySelector('.order__pickup-row svg');

        areaWrap.innerHTML = '';
        areaWrap.style.display = 'none';
        svgItem.style.display = 'none';
        areaWrap.remove()
    }

    
}


$(document).on('click', '.order__pickup-row', function() {
    
    $('.order__pickup-areas').slideToggle();
})

  
$(document).on('click', '.order__input-dropdown', function() {
    var order = JSON.parse(localStorage.getItem('order'));
    var value = $(this).val();
    // console.log(value)

    $('.order__pickup-areas-input').val(value);

    $('.order__pickup-areas').slideToggle();

    order.address_pickup = value;
    localStorage.setItem('order', JSON.stringify(order));


})
  
 
  
  
  
  
  
  
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
          'delivery_address': '',
          
      }
  
      if (!zones_delivery) {
          data = {
              'price_delivery': storedSettingsJson.price_delivery,
              'free_delivery': storedSettingsJson.free_delivery,
              'min_delivery': storedSettingsJson.min_delivery,
              'first_delivery': 0,
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
  
  

  function deliveryUpdate() {
    let deliveryPriceJson = JSON.parse(localStorage.getItem('deliveryPrice'));

    
    
    
    document.getElementById("free_delivery").innerText = deliveryPriceJson.free_delivery + '₽';
    
    
    
  }
  
  
  
  
  // Обновление времени доставки из настроек
  function deliveryTimeUpdate() {
      var storedSettingsJson = JSON.parse(localStorage.getItem('shopSettings'));
      if (!storedSettingsJson) {
          fetchAndSaveSettings();
      }
      var work_hours = storedSettingsJson.work_hours;
      
  
      count = 0
      work_hours.forEach(function(item) { 
          // Создаем элемент для дня
          var dayElement = document.createElement('div');
          dayElement.classList.add('order__times-drop-day');
          dayElement.classList.add('drop_item');
  
  
          dayElement.textContent = item.while;
          dayElement.textContent = item.while;
          dayElement.id = `day-${count}`;
          dayElement.setAttribute('data-id', count);
  
          // Добавляем элемент дня в родительский контейнер для дней
          document.getElementById('day_items').appendChild(dayElement);
  
          // Создаем элементы времени для текущего дня
          var timeElementWrapper = document.createElement('div');
  
          timeElementWrapper.classList.add('order__times-drop-time-wrap');
          
          if (count == 0) {
              timeElementWrapper.classList.add('order__times-drop-time-wrap--active');
          }
  
          timeElementWrapper.id = `time-${count}`;
          timeElementWrapper.setAttribute('data-id', count); 
          
          item.times.forEach(function(time) {
              if (count == 0 && time == "Как можно скорее") {
                  return
              }
              var timeElement = document.createElement('div');
              timeElement.classList.add('order__times-drop-time-item');
              timeElement.classList.add('drop_item');
              timeElement.textContent = time;
  
              
  
              timeElementWrapper.appendChild(timeElement);
          });
  
          // Добавляем элементы времени в родительский контейнер для времени
          document.getElementById('time_items').appendChild(timeElementWrapper);
          count += 1
      });
  }
  


// Динамическое добавление полей в order

function addOrderFields() {

    // Получаем объект order из локального хранилища
    let order = JSON.parse(localStorage.getItem('order'));

    

    

    // При загрузке страницы устанавливаем сохраненные значения в поля ввода, если они есть
    $('.order__input').each(function() {
        let dataName = $(this).data('name'); // Получаем значение атрибута 'data-name'
        
        // if (!$(this.hasClass('.order__input-login'))) {

        // }
        // Проверяем, есть ли соответствующее значение в объекте order
        if (order && order[dataName] !== undefined) {
            // Устанавливаем значение в поле ввода
            $(this).val(order[dataName]);
        }
    });

    // Применяем маску для поля ввода телефонного номера при фокусе на нем
    $(document).on('focus', '.phone', function(e) {
        $(this).mask("+7 (999) 999 99-99");
    });
};
addOrderFields()

// Обработчик события change для каждого поля ввода
$('.order__input').on('change input', function() {
    let dataName = $(this).data('name'); // Получаем значение атрибута 'data-name'
    let value = $(this).val(); // Получаем значение поля ввода
    let order = JSON.parse(localStorage.getItem('order'));
    

    // Обновляем соответствующее значение в объекте order
    order[dataName] = value;

    let hasEmptyFields = hasEmptyFieldsCheck();

    if (hasEmptyFields) {
        if ($('.order__next').hasClass('order__next--error')) {

            $('.order__next').text('Заполните обязательные поля');
            $('.order__next').addClass('order__next--error');
        }
        
    } else if (dataName != 'pay_change' && dataName != 'order_conmment') {
        $('.order__next').text('Далее');
        $('.order__next').removeClass('order__next--error');
    }

    
    $(this).removeClass('order__input--error');

    // Сохраняем обновленный объект order в локальное хранилище
    localStorage.setItem('order', JSON.stringify(order));

    // console.log(order)
    
    
});


// приборы
$(document).on('click', '.order__checkup-cutlery-btn', function() {
    
    let cutlery = parseInt($(this).closest('.order__checkup-cutlery').find('.order__input').val())
    

    if($(this).hasClass('minus')) {
        

        if (cutlery > 0) {

            cutlery = cutlery - 1
        }
    } else {
        cutlery = cutlery + 1
    }
    $(this).closest('.order__checkup-cutlery').find('.order__input').val(cutlery)
    $(this).closest('.order__checkup-cutlery').find('.order__input').val(cutlery).change();
    // console.log(optionsIds)
    
})



// Функции математики в корзине


function getTotalPriceToBallMath(exclude_combos) {
    
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    let order = JSON.parse(localStorage.getItem('order'));
    
    let totalPrice = 0;

    

    for (let itemId in cart) {
        let item = cart[itemId];


        if (item.type == 'combo' && exclude_combos==true) {
            totalPrice += 0
        } else {
            totalPrice += item.price * item.quantity;
        }

        
        
    }

    totalPrice = totalPrice - getAllDiscount()

    
    
    
    return totalPrice
}




// считаем доступные баллы
function maxBallsPay() {
    

    let loyalCart = JSON.parse(localStorage.getItem('loyalCart'));
    let order = JSON.parse(localStorage.getItem('order'));
    let daliveryType = localStorage.getItem("deliveryType");

    // console.log(order)
    
    // console.log(daliveryType);

    let order_balls = order.bonuses_pay;

    let balls = loyalCart.cart_balls - order_balls;

    let balls_min_summ = loyalCart.balls_min_summ;
    let exclude_combos = loyalCart.exclude_combos;
    let exclude_sales = loyalCart.exclude_sales;

    let percent_pay = loyalCart.percent_pay;
    let percent_pay_pickup = loyalCart.percent_pay_pickup;



    let total_price = getTotalPriceToBallMath(exclude_combos);



    
    let max_active_balls = 0;

    if (daliveryType == '1') {

        max_active_balls = total_price / 100 * percent_pay;

    } else {
        max_active_balls = total_price / 100 * percent_pay_pickup;
    }

    if (total_price - max_active_balls <= balls_min_summ) {
        max_active_balls = total_price - balls_min_summ;
    }

    if (max_active_balls >= balls) {
        max_active_balls = balls;
    }

    if (max_active_balls < 0) {
        max_active_balls = 0;
    }
    max_active_balls = Math.floor(max_active_balls);
    // console.log(total_price, percent_pay_pickup, percent_pay, balls, max_active_balls);
    
    // console.log(max_active_balls,order_balls)
    let innerHtml = '';
    if (max_active_balls > 0 && order_balls == 0) {
        innerHtml = `
        <div class="order__info-item" >
            <p>Баллов на счету:</p>
            <div>${balls}₽</div>
        </div>
        <div class="order__info-item">
            <p><small>Списать ${max_active_balls} суммы покупки баллами?</small></p>
            <div><a href="#" id="balls-pay" class="order__info-link">Списать баллы</a></div>
        </div>
        `
    } else if(order_balls > 0) {
        innerHtml = `
        <div class="order__info-item" >
            <p>Баллов на счету:</p>
            <div>${balls}₽ (-${order_balls}) <div><a href="#" id="balls-refresh" class="order__info-link">Отменить</a></div></div>
        </div>
       
        `
    }
    

    $('#balls').html(innerHtml);
    
    

    return max_active_balls

}
// maxBallsPay()
// активировать баллы

$(document).on('click','.active_balls', function(e) {
    e.preventDefault();
    setLoyalCart();
    maxBallsPay()
    getTotalPriceAfterDiscount();
    $(this).remove();
})

$(document).on('click','#balls-pay', function(e) {
    e.preventDefault();
    let max_active_balls = maxBallsPay();
    let order = JSON.parse(localStorage.getItem('order'));
    order.bonuses_pay = max_active_balls;
    localStorage.setItem('order', JSON.stringify(order));
    maxBallsPay()
    getTotalPriceAfterDiscount();
    // $('#balls').remove();
})

$(document).on('click','#balls-refresh', function(e) {
    e.preventDefault();
    refreshBalls();
    getTotalPriceAfterDiscount();
    
})

// сбросить баллы
function refreshBalls() {
    let order = JSON.parse(localStorage.getItem('order'));
    order.bonuses_pay = 0;
    localStorage.setItem('order', JSON.stringify(order));
    maxBallsPay()
    getTotalPriceAfterDiscount();
}

// refreshBalls()

// Сумма всех скидок
function getAllDiscount() {
    let deliveryType = localStorage.getItem("deliveryType"); 

    let shopSettings = JSON.parse(localStorage.getItem('shopSettings'));
    let discountOnPickup = shopSettings.discount_on_pickup;

    let discountOnFirstDelivery = JSON.parse(localStorage.getItem('deliveryPrice')).first_delivery;

    let first_delivery_summ = getTotalPrice() * discountOnFirstDelivery / 100;

    let sale_persent = 0;

    

    // Округляем сумму скидки первой доставки
    first_delivery_summ = Math.floor(first_delivery_summ);

    if (shopSettings.summ_discount == true && deliveryType == '0') {
        first_delivery_summ = 0;
    }

    if (first_delivery_summ != 0) {
        document.getElementById("discountOnFirstDelivery").innerText = `${first_delivery_summ}₽ (${discountOnFirstDelivery}%)`;
        document.getElementById("first_delivery_discount_info").style.display = 'flex';
        sale_persent = sale_persent + discountOnFirstDelivery;
    } else {
        document.getElementById("discountOnFirstDelivery").innerText = '';
        document.getElementById("first_delivery_discount_info").style.display = 'none';
    }
    
    let summ = 0;

    if (deliveryType == '0' && discountOnPickup != 0) {
        let pickup_discount = getTotalPrice() * discountOnPickup / 100;
        // Округляем сумму скидки при самовывозе
        pickup_discount = Math.floor(pickup_discount);
        summ = summ + pickup_discount;

        document.getElementById("discountOnPickup").innerText = `${pickup_discount}₽ (${discountOnPickup}%)`;
        document.getElementById("pickup_discount_info").style.display = 'flex';
        sale_persent = sale_persent + discountOnPickup;
    } else {
        document.getElementById("discountOnPickup").innerText = '';
        document.getElementById("pickup_discount_info").style.display = 'none';
    }

    summ = summ + first_delivery_summ;


    let order = JSON.parse(localStorage.getItem('order'));
    order.sale_percent = sale_persent
    localStorage.setItem('order', JSON.stringify(order));


    


    // добавляем к сумме скидок заказа активные баллы
    
    let active_balls = order.bonuses_pay

    summ = summ + active_balls

    // console.log(summ)

    return summ;
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
getTotalPrice()

// Дополнительные наценки в корзине
function getDopItems() {

    let deliveryType = localStorage.getItem("deliveryType");
    

    return fetch('/api/v1/dop_items/')
        .then(response => response.json())
        .then(data => {
            let summ = 0;
            let itemsHTML = ''; // Строка для хранения HTML-кода элементов
            data.forEach(function(item) {
                let price = parseFloat(item['price']).toFixed(2); // Форматируем цену до двух знаков после запятой
                price = price.replace(/(\.0+|0+)$/, '');
                let name = item['name'];
                let description = item['description'];

                let delivery = item['delivery'];
                let pickup = item['pickup'];

                if (deliveryType == '1' && delivery) {
                    summ = summ + parseFloat(price);
                
                    // Создаем HTML-код для текущего элемента
                    let itemHTML = `
                        <div class="dop-item">
                            <div class="dop-item__wrap">
                                <h3>${name}</h3>
                                <p class="dop-item__description">${description}</p>
                            </div>
                                <p class="dop-item__price">${parseFloat(price)}₽</p>
                        </div>
                    `;
                    itemsHTML += itemHTML; // Добавляем HTML-код элемента к общей строке

                }
                if (deliveryType == '0' && pickup) {
                    summ = summ + parseFloat(price);
                
                    // Создаем HTML-код для текущего элемента
                    let itemHTML = `
                        <div class="dop-item">
                            <div class="dop-item__wrap">
                                <h3>${name}</h3>
                                <p class="dop-item__description">${description}</p>
                            </div>
                                <p class="dop-item__price">${parseFloat(price)}₽</p>
                        </div>
                    `;
                    itemsHTML += itemHTML; // Добавляем HTML-код элемента к общей строке

                }

                
                
            });
            
            // Добавляем собранный HTML-код всех элементов в контейнер с id="dop_items_container"
            document.getElementById('dop_items_container').innerHTML = itemsHTML;
            
            return summ;
        })
        .catch(error => {
            console.error('Ошибка загрузки:', error);
            return 0; // Возвращаем 0 в случае ошибки
        });
}


// Общая сумма с доставкой и скидками
function getTotalPriceAfterDiscount() {
    Promise.all([getTotalPrice(), getDopItems(), getDeliverySumm(), getAllDiscount()])
        .then(([totalPrice, dopItemsSum, deliverySumm, allDiscount]) => {
            let res = totalPrice + dopItemsSum + deliverySumm - allDiscount;
            document.getElementById("total_price_after_discount").innerText = res + '₽';
            let order = JSON.parse(localStorage.getItem('order'));
            order.summ = res;
            localStorage.setItem('order', JSON.stringify(order));
            // console.log(res);
            return res;
        })
        .catch(error => {
            // Обработка ошибок
            console.error('Ошибка:', error);
        });
}


function getMinimalDelivery() {

    let delivery = JSON.parse(localStorage.getItem('deliveryPrice'));

    let minimalDelivery = delivery.min_delivery
    let totalPrice = getTotalPrice()

    let deliveryType = localStorage.getItem("deliveryType");


    if (totalPrice < minimalDelivery && deliveryType == '1') {
        
        $('.order__bottom').hide()
        $('.order__checkup-item').hide()

        var text = `

        <div class="cart__empty cart__min">

        <svg width="217" height="217" viewBox="0 0 217 217" fill="none" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <rect width="217" height="217" fill="url(#pattern0)"/>
        <defs>
        <pattern id="pattern0" patternContentUnits="objectBoundingBox" width="1" height="1">
        <use xlink:href="#image0_80_2" transform="scale(0.00195312)"/>
        </pattern>
        <image id="image0_80_2" width="512" height="512" xlink:href="data:image/png;base64,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"/>
        </defs>
        </svg>

        <p>Минимальная сумма для оформления заказа составляет <b>${minimalDelivery} ₽</b></p>
        <a href="#" class="cart__min-btn open_cart">Посмотреть корзину</a>
        </div>

        `
        $('#cart__min').html(text)
        
    } else {

        $('.cart__min').remove()
        $('.order__bottom').show()
        $('.order__checkup-item').show()
    }





    return minimalDelivery
}





// Возвращаем финальную стоимость доставки с учетом способа доставки и условий
function getDeliverySumm() {
    

    let delivery = JSON.parse(localStorage.getItem('deliveryPrice'));
    let summ = 0
    // console.log(delivery)
    if (delivery.free_delivery > getTotalPrice()) {
        summ = delivery.price_delivery
    } else {
        summ = 0
    }

    var deliveryType = localStorage.getItem("deliveryType");

    

    
    if (deliveryType === "0") {
        summ = 0
    }
    
    
    if (summ == 0 | delivery.free_delivery == 999999) {

        document.getElementById("free_delivery_info").style.display = 'none';
    } else {

        document.getElementById("free_delivery_info").style.display = 'flex';
    }


    document.getElementById("total_delivery").innerText = summ + '₽';


    let order = JSON.parse(localStorage.getItem('order'));
    order.delivery_price = summ

    localStorage.setItem('order', JSON.stringify(order));

    

    return summ

}


// Количество товаров в корзине
function getTotalCount() {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    let totalCount = 0

    for (let itemId in cart) {
        let item = cart[itemId];
        

        totalCount += item.quantity;
        
    }

    return totalCount

}

// console.log(getDeliverySumm())








// Обработка нажатий кнопок


$(document).on('click','.cart__btn, .open_cart',function(e){
    e.preventDefault();
    $('.cart').addClass('cart--active')
    $('body').addClass('body')
    
})

$(document).on('click','.cart__owerlay, .cart__closer',function(e){
    e.preventDefault()

    $('.cart').removeClass('cart--active');
    
  

    
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
    let target = event.target;
    let setupAddress = document.getElementById("set_delivery");
    if (target === setupAddress) {
        document.getElementById("check-delivery").style.display = 'flex';
    }
});


$(document).on('click','.order__checkup',function(e){
    e.preventDefault();
    $('.order').addClass('order--active');
    $('body').addClass('body');
    $('.cart').removeClass('cart--active');

    
})

$(document).on('click','.order__closer, .order__owerlay',function(e){
    e.preventDefault();
    $('.order').removeClass('order--active')
    $('body').removeClass('body');

})



$(document).on('click','.show-map',function(e){
    $('#setup-address').css('display', 'flex');
})



$(document).on('click','.order__times-active',function(){
    
    $('.order__times-drop').toggleClass('order__times-drop--active')
    $('.order__times-drop-owerlay').toggleClass('order__times-drop-owerlay--active')

})

$(document).on('click','.order__times-drop-owerlay',function(){

    $('.order__times-drop').removeClass('order__times-drop--active')
    $('.order__times-drop-owerlay').removeClass('order__times-drop-owerlay--active')
})



$(document).on('click', '.order__times-drop-day', function(e){
    let day = $(this).text();
    let order = JSON.parse(localStorage.getItem('order')) || {}; // Проверка на null
    order.day = day;
    
    localStorage.setItem('order', JSON.stringify(order)); // Сохранение обновленного объекта
    setOrder();

    $('.order__times-drop-day').removeClass('drop_item--active')    
    $(this).addClass('drop_item--active')


    let dataId = $(this).attr('data-id');
    $('.order__times-drop-time-wrap').removeClass('order__times-drop-time-wrap--active');
    $('.order__times-drop-time-wrap[data-id="' + dataId + '"]').addClass('order__times-drop-time-wrap--active');
    


});

$(document).on('click', '.order__times-drop-time-item', function(e){
    let time = $(this).text();
    let order = JSON.parse(localStorage.getItem('order')) || {}; // Проверка на null
    order.time = time;
    
    localStorage.setItem('order', JSON.stringify(order)); // Сохранение обновленного объекта
    setOrder();

    $('.order__times-drop-time-item').removeClass('drop_item--active')    
    $(this).addClass('drop_item--active')



    $('.order__times-drop').removeClass('order__times-drop--active')
    $('.order__times-drop-owerlay').removeClass('order__times-drop-owerlay--active')
});


$(document).on('click', '#checkout__radio-now', function(e){
    let order = JSON.parse(localStorage.getItem('order')) || {}; // Проверка на null
    order.data_time = 0;
    order.day = 'Сегодня';
    order.time = 'Как можно скорее';
    
    localStorage.setItem('order', JSON.stringify(order)); // Сохранение обновленного объекта

    $('.order__times-drop').removeClass('order__times-drop--active')
    setOrder();
    
})

$(document).on('click', '#checkout__radio-bytime', function(e){
    let order = JSON.parse(localStorage.getItem('order')) || {}; // Проверка на null
    order.data_time = 1;
    
    localStorage.setItem('order', JSON.stringify(order)); // Сохранение обновленного объекта
    setOrder();
    
})


// Перебор всех товаров на странице и поиск их в корзине
function checkProducts() {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let products = document.querySelectorAll('.btn-wrap');

    // $('.cart__maby').load(location.href + " .cart__maby-refresh");
    
    products.forEach(function(product) {
        let id = product.getAttribute('data-cart-id');

        let type = product.getAttribute('data-type');
        let optionsIdString = product.getAttribute('data-optionsid');
        let optionsIdArray = optionsIdString.split(",").filter(optionId => optionId.trim() !== "").map(optionId => parseInt(optionId.trim(), 10));


        if (type === 'product') {
            id += '000';
        } else if (type === 'combo') {
            id += '111';
        } else if (type === 'constructor') {
            id += '222';
        } 

        id += optionsIdArray.join('');

        let productListItem = product.querySelector('.btn-wrap__count');
        let productSvgItem = product.querySelector('.btn-wrap__svg');

        let productBtn = product.querySelector('.add_to_cart');

        if (!productBtn) {
            productBtn = product.querySelector('.combo-popup__btn');
        }

        


        if (cart[id]) {

            if (product.closest('.product-list__item').classList.contains('product-list__item--mini')) {
                let product_item = product.closest('.product-list__item');
                product_item.style.display = 'none';
            } else {
                
            
                let inHTML = `
                <div class="cart__items-wrap">
                    <div class="cart__btn-wrapper">
                        <button class="cart__plusminus" data-action="minus" data-id="${id}">-</button>
                        <div class class="cart__quantity">${cart[id].quantity}</div>
                        <button class="cart__plusminus" data-action="plus" data-id="${id}">+</button>
                    </div>
                </div>
                `;

                let svgHTML = `
                    <div class="cart__svg">
                        <?xml version="1.0" ?><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><defs><style>.cls-1{fill:#101820;}</style></defs><title/><g data-name="Layer 28" id="Layer_28"><path class="cls-1" d="M16,31A15,15,0,1,1,31,16,15,15,0,0,1,16,31ZM16,3A13,13,0,1,0,29,16,13,13,0,0,0,16,3Z"/><path class="cls-1" d="M13.67,22a1,1,0,0,1-.73-.32l-4.67-5a1,1,0,0,1,1.46-1.36l3.94,4.21,8.6-9.21a1,1,0,1,1,1.46,1.36l-9.33,10A1,1,0,0,1,13.67,22Z"/></g></svg>
                        <p>В корзине</p>
                    </div>
                    `

                product.classList.add('in-cart');
                
                productBtn.style.display = 'none';
                productListItem.innerHTML = inHTML;
                productSvgItem.innerHTML = svgHTML;
                
            }
        } else {
            let product_item = product.closest('.product-list__item');
            product_item.style.display = 'flex';
            product.classList.remove('in-cart');
           
           
            
            productBtn.style.display = 'block';
                
            productListItem.innerHTML = '';
            productSvgItem.innerHTML = '';
                
            
        }
        

        



    })

}
checkProducts()

$(document).on('change', 'input[type="checkbox"], input[type="radio"]', function(){
    checkProducts()
}) 

$(document).on('click','.product-options__item',function(e){

    
    var id = $(this).attr('data-id')
    var price = parseFloat($(this).attr('data-price'))
    var value = $(this).attr('data-value')
    var product_id = $(this).attr('data-product-id')
    var image = $(this).attr('data-image')
    var weight = $(this).attr('data-weight')
    var $productItem = $(this).closest('.product-list__item');


    
    $productItem.find('input[type="checkbox"], input[type="radio"]').prop('checked', false);
    

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

    $productItem.find('.btn-wrap').attr('data-price', res_price).attr('data-optionsid', id)

    $productItem.find('.product-list__price').html(res_price + ' ₽')
    $productItem.find('.product-list__old').html(res_old_price + ' ₽')


    $productItem.find('.product-options-popup__options-select-wrap').find('.product-options-popup__options-select').removeClass('product-options-popup__options-select--active')
    $productItem.find('.product-options-popup__options-select-wrap').find(`[data-id='${id}']`).addClass('product-options-popup__options-select--active')

    $productItem.find('.product-options-popup__price').attr('data-price', res_price)
    $productItem.find('.product-options-popup__old-price').attr('data-price', res_old_price)

    $productItem.find('.product-options-popup__price').text(res_price + ' ₽')
    $productItem.find('.product-options-popup__old-price').text(res_old_price + ' ₽')

    // .product-options-popup_btn
    $productItem.find('.product-options-popup_btn').attr('data-price', res_price).attr('data-optionsid', id)
    

    
    
    checkProducts()
    // $productItem.find('.product-options__span-'+product_id).html(value)

});


// Добавление в корзину
$(document).on('click', '.add_to_cart', function(){
    let $button = $(this);
    let id = $button.parent('.btn-wrap').attr('data-cart-id');
    let type = $button.parent('.btn-wrap').attr('data-type');
    let optionsIdString = $button.parent('.btn-wrap').attr('data-optionsid');
    let price = $button.parent('.btn-wrap').attr('data-price');
    let name = $button.parent('.btn-wrap').attr('data-name');
    let image = $button.parent('.btn-wrap').attr('data-image');
    
    let parent = $button.closest('.product-list__item');
    if (parent.hasClass('product-list__item--mini')) {
        $('.product-options-popup').removeClass('product-options-popup--active')
    }

    addToCart(id, name, price, image, optionsIdString, type);
    
   
});


$(document).on('click','.combo-popup__btn',function(){
    let $button = $(this);
    let id = $(this).parent('.btn-wrap').attr('data-cart-id')
    let type = $button.parent('.btn-wrap').attr('data-type');
    let optionsIdString = $button.parent('.btn-wrap').attr('data-optionsid');
    let price = $button.parent('.btn-wrap').attr('data-price');
    let name = $button.parent('.btn-wrap').attr('data-name');
    let image = $button.parent('.btn-wrap').attr('data-image');

    if ($(this).hasClass('combo-popup__btn--active')) {
        addToCart(id, name, price, image, optionsIdString, type);
        

    } else {
        
        return
    }
})



function hasEmptyFieldsCheck() {
    let hasEmptyFields = false;
    // Проверяем каждое поле ввода с классом "required"
    $('.order__input.required').each(function() {

        // Проверяем, является ли поле с именем "address" обязательным для заполнения

        if ($(this).attr('name') !== 'address' || !$(this).closest('.order__next').hasClass('order__next--pickup')) {
            // Если поле не является обязательным для заполнения или это не кнопка "pickup",
            // то проверяем его на пустоту и добавляем класс "error" при необходимости
            if ($(this).val().trim() === '') {
                $(this).addClass('order__input--error');
                hasEmptyFields = true;
            } else {
                // Если поле не пустое и имеет класс "error", удаляем класс "error"
                $(this).removeClass('order__input--error');
            }
        }
        // Проверяем, есть ли у поля атрибут data-login="false" и добавляем класс "error" при необходимости
        if ($(this).data('login') === false) {
            $(this).addClass('order__input--error');
            hasEmptyFields = true;
        }
    });

    // Проверяем каждый checkbox с классом "required"
    $('.required_checkbox').each(function() {
        // Если checkbox не отмечен, добавляем класс "error" и устанавливаем hasEmptyFields в true
        if (!$(this).is(':checked')) {
            $(this).parent('label').addClass('required_checkbox--error');
            hasEmptyFields = true;
        } else {
            // Если checkbox отмечен и имеет класс "error", удаляем класс "error"
            $(this).parent('label').removeClass('required_checkbox--error');
        }
    });

    

    return hasEmptyFields

}


// Обработка обязательных полей
$(document).on('click', '.order__next', function(e) {
    e.preventDefault();
    
    // Переменная для отслеживания пустых полей
    let hasEmptyFields = hasEmptyFieldsCheck();

    // Если есть пустые поля, выводим сообщение или выполняем действие
    if (hasEmptyFields) {
        // Здесь можно выполнить действие, например, показать сообщение об ошибке или что-то еще
        $('.order__next').text('Заполните обязательные поля');
        $('.order__next').addClass('order__next--error');

        $('.order__pay-methods').hide()
        $('.order__body-wrap').show()


    } else {

        let htmlInner = 
        `
        <a href="#" class="btn order__back">Назад</a>
        <a href="#" class="btn btn--primary order__next order_create">Оформить</a>
        `

        $('.order .checkout__counter-item:nth-child(2)').addClass('checkout__counter-item--active checkout__counter-item--line');
        $('.order .checkout__counter-item:nth-child(1)').addClass('checkout__counter-item--line');

        $('.order__next-wrap').html(htmlInner)
        $('.order__next-wrap').addClass('order__next-wrap--flex')

        $('.order__body-wrap').hide()

        $('.order__pay-methods').show()
        
    }

    
    getTotalPriceAfterDiscount();
});


$(document).on('click', '.order_create', function(e) {
    e.preventDefault();
    let order = localStorage.getItem('order') || {}; // Проверка на null
    let cart = localStorage.getItem('cart') || {}; // Проверка на null



    $('.order__load').addClass('order__load--active')

    // console.log(order)

    let csrfToken = $('input[name="csrfmiddlewaretoken"]').val();

    data = {
        csrfmiddlewaretoken: csrfToken,
        'order': order,
        'cart': cart
    }

    


    $.ajax({
        method: "POST",
        url: "/orders/create/fast/",
        data: data,
        dataType: "json",
        success: function(responseData) {
            // console.log(responseData); // Выводим ответ в консоль

            if (responseData && responseData.confirmation_url) {
                // Получаем значение confirmation_url из responseData
                let confirmationUrl = responseData.confirmation_url;
                // Выполняем редирект на указанный URL

                let order = JSON.parse(localStorage.getItem('order'));
                data = {
                    'show': true,
                    'order_id': responseData.order_id,
                    'user_name': order.user_name,
                    'user_phone': order.user_phone,
                    'address': order.address,
                    'address_pickup': order.address_pickup,
                    'address_comment': order.address_comment,
                    'delivery_type': order.delivery_type,
                    'entrance': order.entrance,
                    'floor': order.floor,
                    'flat': order.flat,
                    'door_code': order.door_code,
                    
                    'day': order.day,
                    'time': order.time,
                    'pay_method': order.pay_method,
                    'pay_change': order.pay_change,
                    'delivery_method': order.delivery_method,
                    'delivery_price': order.delivery_price,
                    'order_conmment': order.order_conmment,
                    
                    'summ': order.summ,
                    
                    'status': 'Новый',
                    
                }

                // Обновление или удаление данных из localStorage
                localStorage.removeItem('order');
                localStorage.removeItem('cart');
                localStorage.removeItem('lastOrder');
                

                localStorage.setItem('lastOrder', JSON.stringify(data));

                order.address = '';
                localStorage.setItem('order', JSON.stringify(order));

                $('.order__load').removeClass('order__load--active')
                $('.odred-done').addClass('odred-done--active')
                $('.order').removeClass('order--active')
                
                getLastOrder()

                updateAll()

                // window.location.href = confirmationUrl;
               


            } else {
                console.error('Ответ не содержит confirmation_url');
                // Обработка случаев, когда нет confirmation_url в ответе
            }
            // Здесь вы можете обрабатывать полученные данные
        },
        error: function(xhr, status, error) {
            console.error(xhr.responseText); // Выводим сообщение об ошибке в консоль
        }
    });

})

// проверка последнего заказа
jQuery(document).ready(function () {
    let last_order = JSON.parse(localStorage.getItem('lastOrder'));
    let shopSettings = JSON.parse(localStorage.getItem('shopSettings'));
    
    // console.log(last_order)
    
    if (last_order && last_order.status != 'Выполнен' && last_order.status != 'Отказ' && shopSettings.check_order_status) {
        let order_id = last_order.order_id; // предположим, что id заказа доступен в last_order
        let intervalId; // переменная для хранения идентификатора интервала

        // console.log(last_order)
        $('.popup-order-status').css('display', 'flex')
        function updateOrderStatus() {
            $.ajax({
                url: '/api/v1/get_order_status/' + order_id + '/',
                method: 'GET',
                success: function(data) {
                    
                    last_order.status = data.status;
                    localStorage.setItem('lastOrder', JSON.stringify(last_order));
                    // Обновление popup с полученными данными
                    updatePopup(data.status_list, data.status);
    
                    // Проверка на выполненный статус
                    if (data.status === 'Выполнен') {
                        
                        clearInterval(intervalId); // Остановка повторения запросов
                    }
                    // Проверка на выполненный статус
                    if (data.status === 'Отказ') {
                        $('.popup-order-status').css('display', 'none')
                        clearInterval(intervalId); // Остановка повторения запросов
                    }
                },
                error: function(xhr, status, error) {
                    console.error('Ошибка при получении статуса заказа:', error);
                }
            });
        }
    
        function updatePopup(status_list, current_status) {
            // Очистка текущего содержимого popup
            // и добавление новых пунктов списка статусов
            let popupContent = '';
            status_list.forEach(function(status) {
                let activeClass = (status === current_status) ? 'status-item--active' : '';
                let svg = getSVGByStatus(status); // Получение SVG для статуса
                popupContent += '<div title="' + status + '" class="status-item ' + activeClass + '">' + status + svg + '</div>';
            });
            $('#popup-order-status').html(popupContent);
        }
    
        function getSVGByStatus(status) {
            // Возвращает SVG в зависимости от статуса
            switch (status) {
                case 'Новый':

                    

                    return `
                        <?xml version="1.0" encoding="UTF-8" standalone="no"?>
                        <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                        <svg width="800px" height="800px" viewBox="0 0 32 32" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:sketch="http://www.bohemiancoding.com/sketch/ns">
                            
                            <title>new</title>
                            <desc>Created with Sketch Beta.</desc>
                            <defs>

                        </defs>
                            <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd" sketch:type="MSPage">
                                <g id="Icon-Set" sketch:type="MSLayerGroup" transform="translate(-516.000000, -99.000000)" fill="#000000">
                                    <path d="M527.786,122.02 L522.414,125.273 C521.925,125.501 521.485,125.029 521.713,124.571 L524.965,119.195 L527.786,122.02 L527.786,122.02 Z M537.239,106.222 L540.776,109.712 L529.536,120.959 C528.22,119.641 526.397,117.817 526.024,117.444 L537.239,106.222 L537.239,106.222 Z M540.776,102.683 C541.164,102.294 541.793,102.294 542.182,102.683 L544.289,104.791 C544.677,105.18 544.677,105.809 544.289,106.197 L542.182,108.306 L538.719,104.74 L540.776,102.683 L540.776,102.683 Z M524.11,117.068 L519.81,125.773 C519.449,126.754 520.233,127.632 521.213,127.177 L529.912,122.874 C530.287,122.801 530.651,122.655 530.941,122.365 L546.396,106.899 C547.172,106.124 547.172,104.864 546.396,104.088 L542.884,100.573 C542.107,99.797 540.85,99.797 540.074,100.573 L524.619,116.038 C524.328,116.329 524.184,116.693 524.11,117.068 L524.11,117.068 Z M546,111 L546,127 C546,128.099 544.914,129.012 543.817,129.012 L519.974,129.012 C518.877,129.012 517.987,128.122 517.987,127.023 L517.987,103.165 C517.987,102.066 518.902,101 520,101 L536,101 L536,99 L520,99 C517.806,99 516,100.969 516,103.165 L516,127.023 C516,129.22 517.779,131 519.974,131 L543.817,131 C546.012,131 548,129.196 548,127 L548,111 L546,111 L546,111 Z" id="new" sketch:type="MSShapeGroup">

                        </path>
                                </g>
                            </g>
                        </svg>
                    `;
                case 'Готовится':
                    return `
                        <?xml version="1.0" ?>

                        <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                        <svg fill="#000000" width="800px" height="800px" viewBox="0 0 128 128" xmlns="http://www.w3.org/2000/svg">

                        <title/>

                        <g id="Grid">

                        <path d="M82.38,113.13H44.62a10.46,10.46,0,0,1-10.44-10.45V80.38a21.38,21.38,0,0,1,5.48-42,21,21,0,0,1,2.63.17,21.14,21.14,0,0,1-.16-2.64,21.37,21.37,0,0,1,42.74,0,21.14,21.14,0,0,1-.16,2.64,21,21,0,0,1,2.63-.17,21.38,21.38,0,0,1,5.48,42v22.3A10.46,10.46,0,0,1,82.38,113.13ZM39.66,41.34A18.38,18.38,0,0,0,36,77.72a1.49,1.49,0,0,1,1.2,1.47v23.49a7.45,7.45,0,0,0,7.44,7.45H82.38a7.45,7.45,0,0,0,7.44-7.45V79.19A1.49,1.49,0,0,1,91,77.72a18.38,18.38,0,0,0-3.68-36.38,18,18,0,0,0-4.14.48A1.5,1.5,0,0,1,81.39,40a18,18,0,0,0,.48-4.15,18.37,18.37,0,0,0-36.74,0A18,18,0,0,0,45.61,40a1.5,1.5,0,0,1-1.81,1.8A18,18,0,0,0,39.66,41.34Z"/>

                        <path d="M92.64,119.5H34.36a1.5,1.5,0,0,1,0-3H92.64a1.5,1.5,0,0,1,0,3Z"/>

                        <path d="M67.47,105.18a1.51,1.51,0,0,1-1.5-1.5V71.88a1.5,1.5,0,0,1,3,0v31.8A1.5,1.5,0,0,1,67.47,105.18Z"/>

                        <path d="M75.42,105.18a1.5,1.5,0,0,1-1.5-1.5V87.78a1.5,1.5,0,0,1,3,0v15.9A1.5,1.5,0,0,1,75.42,105.18Z"/>

                        </g>

                        </svg>
                    `;

                case 'Готов к доставке':
                    return `
                    
                        <?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                        <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M5 14L8.23309 16.4248C8.66178 16.7463 9.26772 16.6728 9.60705 16.2581L18 6" stroke="#33363F" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    `;
                case 'Готов к выдаче':
                    return `
                    
                        <?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                        <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path d="M5 14L8.23309 16.4248C8.66178 16.7463 9.26772 16.6728 9.60705 16.2581L18 6" stroke="#33363F" stroke-width="2" stroke-linecap="round"/>
                        </svg>
                    `;
                case 'Доставка':

                    return `
                        <?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                        <svg fill="#000000" width="800px" height="800px" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg"><path d="M15.48 12c-.13.004-.255.058-.347.152l-2.638 2.63-1.625-1.62c-.455-.474-1.19.258-.715.712l1.983 1.978c.197.197.517.197.715 0l2.995-2.987c.33-.32.087-.865-.367-.865zM.5 16h3c.277 0 .5.223.5.5s-.223.5-.5.5h-3c-.277 0-.5-.223-.5-.5s.223-.5.5-.5zm0-4h3c.277 0 .5.223.5.5s-.223.5-.5.5h-3c-.277 0-.5-.223-.5-.5s.223-.5.5-.5zm0-4h3c.277 0 .5.223.5.5s-.223.5-.5.5h-3C.223 9 0 8.777 0 8.5S.223 8 .5 8zm24 11c-1.375 0-2.5 1.125-2.5 2.5s1.125 2.5 2.5 2.5 2.5-1.125 2.5-2.5-1.125-2.5-2.5-2.5zm0 1c.834 0 1.5.666 1.5 1.5s-.666 1.5-1.5 1.5-1.5-.666-1.5-1.5.666-1.5 1.5-1.5zm-13-1C10.125 19 9 20.125 9 21.5s1.125 2.5 2.5 2.5 2.5-1.125 2.5-2.5-1.125-2.5-2.5-2.5zm0 1c.834 0 1.5.666 1.5 1.5s-.666 1.5-1.5 1.5-1.5-.666-1.5-1.5.666-1.5 1.5-1.5zm-5-14C5.678 6 5 6.678 5 7.5v11c0 .822.678 1.5 1.5 1.5h2c.676.01.676-1.01 0-1h-2c-.286 0-.5-.214-.5-.5v-11c0-.286.214-.5.5-.5h13c.286 0 .5.214.5.5V19h-5.5c-.66 0-.648 1.01 0 1h7c.66 0 .654-1 0-1H21v-9h4.227L29 15.896V18.5c0 .286-.214.5-.5.5h-1c-.654 0-.654 1 0 1h1c.822 0 1.5-.678 1.5-1.5v-2.75c0-.095-.027-.19-.078-.27l-4-6.25c-.092-.143-.25-.23-.422-.23H21V7.5c0-.822-.678-1.5-1.5-1.5z"/></svg>
                    `;

                case 'Доставлен':
                    return `
                        <?xml version="1.0" encoding="utf-8"?>
                        <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                        <svg width="800px" height="800px" viewBox="0 0 1024 1024" fill="#000000" class="icon"  version="1.1" xmlns="http://www.w3.org/2000/svg"><path d="M959.018 208.158c0.23-2.721 0.34-5.45 0.34-8.172 0-74.93-60.96-135.89-135.89-135.89-1.54 0-3.036 0.06-6.522 0.213l-611.757-0.043c-1.768-0.085-3.563-0.17-5.424-0.17-74.812 0-135.67 60.84-135.67 135.712l0.188 10.952h-0.306l0.391 594.972-0.162 20.382c0 74.03 60.22 134.25 134.24 134.25 1.668 0 7.007-0.239 7.1-0.239l608.934 0.085c2.985 0.357 6.216 0.468 9.55 0.468 35.815 0 69.514-13.954 94.879-39.302 25.373-25.34 39.344-58.987 39.344-94.794l-0.145-12.015h0.918l-0.008-606.41z m-757.655 693.82l-2.585-0.203c-42.524 0-76.146-34.863-76.537-79.309V332.671H900.79l0.46 485.186-0.885 2.865c-0.535 1.837-0.8 3.58-0.8 5.17 0 40.382-31.555 73.766-71.852 76.002l-10.816 0.621v-0.527l-615.533-0.01zM900.78 274.424H122.3l-0.375-65.934 0.85-2.924c0.52-1.82 0.782-3.63 0.782-5.247 0-42.236 34.727-76.665 78.179-76.809l0.45-0.068 618.177 0.018 2.662 0.203c42.329 0 76.767 34.439 76.767 76.768 0 1.326 0.196 2.687 0.655 4.532l0.332 0.884v68.577z" fill="" /><path d="M697.67 471.435c-7.882 0-15.314 3.078-20.918 8.682l-223.43 223.439L346.599 596.84c-5.544-5.603-12.95-8.69-20.842-8.69s-15.323 3.078-20.918 8.665c-5.578 5.518-8.674 12.9-8.7 20.79-0.017 7.908 3.07 15.357 8.69 20.994l127.55 127.558c5.57 5.56 13.01 8.622 20.943 8.622 7.925 0 15.364-3.06 20.934-8.63l244.247-244.247c5.578-5.511 8.674-12.883 8.7-20.783 0.017-7.942-3.079-15.408-8.682-20.986-5.552-5.612-12.958-8.698-20.85-8.698z" fill="" /></svg>
                    `;
                
                case 'Выполнен':
                    return `               
                        <?xml version="1.0" ?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                        <svg width="800px" height="800px" viewBox="0 0 28 28" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.65263 14.0304C6.29251 13.6703 6.29251 13.0864 6.65263 12.7263C7.01276 12.3662 7.59663 12.3662 7.95676 12.7263L11.6602 16.4297L19.438 8.65183C19.7981 8.29171 20.382 8.29171 20.7421 8.65183C21.1023 9.01195 21.1023 9.59583 20.7421 9.95596L12.3667 18.3314C11.9762 18.7219 11.343 18.7219 10.9525 18.3314L6.65263 14.0304Z" fill="#000000"/><path clip-rule="evenodd" d="M14 1C6.8203 1 1 6.8203 1 14C1 21.1797 6.8203 27 14 27C21.1797 27 27 21.1797 27 14C27 6.8203 21.1797 1 14 1ZM3 14C3 7.92487 7.92487 3 14 3C20.0751 3 25 7.92487 25 14C25 20.0751 20.0751 25 14 25C7.92487 25 3 20.0751 3 14Z" fill="#000000" fill-rule="evenodd"/></svg>
                    `;

                // Добавьте другие статусы и их SVG по мере необходимости
                default:
                    return '';
            }
        }
    
        // Инициализация обновления статуса заказа и повторение каждые 2 секунды
        updateOrderStatus();
        intervalId = setInterval(updateOrderStatus, 2000);

    }

    
});



function getLastOrder() {
    var pathname = window.location.href; 
    var origin   = window.location.origin;


    let order = $('#orderDone').attr('data-order')
    let data_title = $('#orderDone').attr('data-title')
    let data_text = $('#orderDone').attr('data-text')

    

    let last_order = JSON.parse(localStorage.getItem('lastOrder'));
    res = pathname.replace(origin, '')
    

    if(last_order) {
        
        
        
        // Преобразуем объект в строку JSON-формата
        let jsonString = JSON.stringify(order);

        // Заменяем символы в строке
        jsonString = jsonString.replace(/'/g, '"'); 
        let newStr = jsonString.slice(1, -1);


        // Преобразуем строку JSON-формата обратно в объект
        let newObj = JSON.parse(newStr);

       
        dataLayer.push(newObj)


        

        


        let order_delivery_items = ''
        let order_delivery_method = ''
        let order_delivery_address = ''

        if (last_order.delivery_method == 'Самовывоз') {
            order_delivery_method = 'самовывоза'
            order_delivery_items = `
                <div class="order__delivery-check-item order-done-delivery">Доставка</div>
                <div class="order__delivery-check-item order-done-pickup order__delivery-check-item--active">Самовывоз</div>
            `
            order_delivery_address = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Точка самовывоза</div>
                    <div class="odred-done__itog-value">${last_order.address_pickup}</div>

                </div>
            `
        } else if (last_order.delivery_method == 'Доставка') {
            order_delivery_method = 'доставки'
            order_delivery_items = `
                <div class="order__delivery-check-item order-done-delivery order__delivery-check-item--active">Доставка</div>
                <div class="order__delivery-check-item order-done-pickup">Самовывоз</div>
            `
            order_delivery_address = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Адрес доставки</div>
                    <div class="odred-done__itog-value">${last_order.address}</div>

                </div>
            `
        }


        let order_comment = ''
        if(last_order.order_conmment) {
            
            order_comment = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Комментарий к заказу</div>
                    <div class="odred-done__itog-value">${last_order.order_conmment}</div>
                </div>
                `
        }

        
        let address_comment = ''
        if(last_order.address_comment) {
            
            address_comment = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Комментарий к адресу</div>
                    <div class="odred-done__itog-value">${last_order.address_comment}</div>
                </div>
                `
        }
        
        let order_flat = ''
        if(last_order.flat) {
            
            order_flat = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Квартира</div>
                    <div class="odred-done__itog-value">${last_order.flat}</div>
                </div>
                `
        }
        let oreder_flore = ''
        if(last_order.floor) {
            
            oreder_flore = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Этаж</div>
                    <div class="odred-done__itog-value">${last_order.floor}</div>
                </div>
                `
        }

        let order_entrance = ''
        if(last_order.entrance) {
            
            order_entrance = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Подъезд</div>
                    <div class="odred-done__itog-value">${last_order.entrance}</div>
                </div>
                `
        }
        let order_door_code = ''
        if(last_order.door_code) {
            
            order_door_code = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Код двери</div>
                    <div class="odred-done__itog-value">${last_order.door_code}</div>
                </div>
                `
        }

        let order_pay_method = ''
        if(last_order.pay_method) {
            
            order_pay_method = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Способ оплаты</div>
                    <div class="odred-done__itog-value">${last_order.pay_method}</div>
                </div>
                `
        }

        let order_pay_change = ''
        if(last_order.pay_change) {
            
            order_pay_change = `
                <div class="odred-done__itog-wrap">
                    <div class="odred-done__itog-data">Сдача c</div>
                    <div class="odred-done__itog-value">${last_order.pay_change}</div>
                </div>
                `
        }
        
        let dataHtml = `       
                <div class="odred-done">

                <div class="odred-done__owerlay"></div>


                <div class="odred-done__container">

                    <div class="odred-done__inner">

                        <div class="odred-done__top">
                        
                            <div class="odred-done__title">
                                Заказ № <span id="odred-done__id">${last_order.order_id}</span>
                            </div>


                            <div class="odred-done__closer">
                                <svg width="26" height="28" viewBox="0 0 26 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M5.85522 5.93945L13.1531 14.0505M13.1531 14.0505L20.451 22.1616M13.1531 14.0505L20.451 5.93945M13.1531 14.0505L5.85522 22.1616" stroke="#333333" stroke-width="1.8766" stroke-linecap="round" stroke-linejoin="round"></path>
                                </svg>
                            </div>

                        </div>
                        


                        

                        <div class="odred-done__body">
                            <div class="order__delivery-check">
                                ${order_delivery_items}
                                
                            </div>

                            <ul class="checkout__counter">
                                <li class="checkout__counter-item checkout__counter-item--active checkout__counter-item--line">
                                    
                                    <span class="checkout__counter-title">Адрес и контакты</span>
                                    <div class="checkout__counter-line-wrap">
                                        <i></i><div class="checkout__counter-line"></div>

                                    </div>
                                
                                </li>
                                <li class="checkout__counter-item checkout__counter-item--active checkout__counter-item--line">

                                    <span class="checkout__counter-title">Оплата</span>
                                    <div class="checkout__counter-line-wrap">
                                    
                                        <div class="checkout__counter-line"></div><i></i><div class="checkout__counter-line"></div>

                                    </div>
                                
                                </li>
                                <li class="checkout__counter-item checkout__counter-item--active checkout__counter-item--line">

                                    <span class="checkout__counter-title">Завершение</span>


                                    <div class="checkout__counter-line-wrap">
                                        
                                        <div class="checkout__counter-line"></div><i></i>
                                    </div>
                                
                                </li>
                            </ul>

                            <div class="odred-done__body-wrap">
                            
                                <p class="odred-done__body-title">${data_title} ${data_text}</p>


                                <div class="odred-done__itog">
                                    <div class="odred-done__itog-item">
                                        <p class="odred-done__itog-title">Итоговые данные</p>


                                        

                                        <div class="odred-done__itog-wrap">
                                            <div class="odred-done__itog-data">Время ${order_delivery_method}</div>
                                            <div class="odred-done__itog-value">${last_order.day} / ${last_order.time}</div>

                                        </div>

                                        ${order_delivery_address}
                                        ${order_flat}
                                        ${oreder_flore}
                                        ${order_entrance}
                                        ${order_door_code}



                                        ${address_comment}


                                        ${order_pay_method}
                                        ${order_pay_change}

                                        ${order_comment}

                                        <div class="odred-done__itog-wrap odred-done__itog-wrap-summ" id="orderDonePrice">
                                            <div class="odred-done__itog-data">Сумма заказа:</div>
                                            <div class="odred-done__itog-value">${last_order.summ} ₽</div>

                                        </div>

                                    </div>


                                </div>


                            </div>

                        </div>
                        
                        

                    </div>
                    <div class="odred-done__bottom">


                    
                        
                        
                    

                    
                        

                    

                        
                    

                        <a href="#" class="btn btn--primary odred-done__ok">Ок</a>

                    

                        
                    </div>

                </div>


                </div>
        `

        
        $('#orderDone').html(dataHtml)

        if(last_order.show == true) {
            $('.odred-done').addClass('odred-done--active')
            $('body').addClass('body');
        } else {
            $('.odred-done').removeClass('odred-done--active')
            $('body').removeClass('body');
        }
        
        
        $(document).on('click','.odred-done__owerlay, .odred-done__ok, .odred-done__closer',function(e){
            $('.odred-done').removeClass('odred-done--active')
            $('body').removeClass('body');
            last_order.show = false
            localStorage.setItem('lastOrder', JSON.stringify(last_order))
            clearCart()
            window.location.href = `/`
            

        })
    }

}
getLastOrder()

$(document).on('click', '.order__back', function(e) {
    e.preventDefault();
    let htmlInner = 
    `
  
    <a href="#" class="btn btn--primary order__next">Далее</a>`

    $('.order__next-wrap').html(htmlInner)
    $('.order__body-wrap').show()
    $('.order__pay-methods').hide()

    $('.order .checkout__counter-item:nth-child(2)').removeClass('checkout__counter-item--active checkout__counter-item--line');
    $('.order .checkout__counter-item:nth-child(1)').removeClass('checkout__counter-item--line');
})

// Убираем возможность снять выбор с обязательных чекбоксов
$(document).ready(function() {
    // Обработчик события click для чекбоксов с классом "no-uncheck"
    $('.required_checkbox').on('click', function(e) {
        e.preventDefault(); // Отменяем действие по умолчанию

        // Проверяем, был ли чекбокс отмечен
        if (!$(this).is(':checked')) {
            $(this).prop('checked', true); // Если не был, отмечаем его
        }
    });
});


// Изменение способа оплаты
$(document).on('change', '.checkout__radio[name="checkoutpayment"]', function(e) {
    
    let order = JSON.parse(localStorage.getItem('order'));
    order.pay_method = $(this).val();
    

    // Получаем простую строку из значения элемента
    let paymentMethod = $(this).val();

    if (paymentMethod.toLowerCase().includes("наличн")) {
        
        $('#pay_change').show();
    } else {
        $('#pay_change').hide();
        $('#pay_change').find('input').val('');
        order.pay_change = '';
    }

    

    localStorage.setItem('order', JSON.stringify(order));
    getTotalPriceAfterDiscount()

    // console.log(order)

    
});



// Проверка номера телефона на первый заказ

$(document).on('keyup', '#check_user_status' ,function(e){
    let phone = $(this).val()
    let min = phone.replace('_', '').replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('+', '')
    
    
    if (min.length == 13) {
        
        var order = JSON.parse(localStorage.getItem('order'));
        order.user_phone = phone;
        localStorage.setItem('order', JSON.stringify(order));


        
        fetch(`/api/v1/first_delivery/${phone}/`)
            .then(response => response.json())
            .then(data => {

                var get_set = JSON.parse(localStorage.getItem('shopSettings'));
                var get_del = JSON.parse(localStorage.getItem('deliveryPrice'));

                
                

                if (data==true) {

                    get_del.first_delivery = get_set.first_delivery;
                    localStorage.setItem('deliveryPrice', JSON.stringify(get_del));
                    

                } else {
                    get_del.first_delivery = 0;
                    localStorage.setItem('deliveryPrice', JSON.stringify(get_del));
                  
                }

                
                var get_del = JSON.parse(localStorage.getItem('deliveryPrice'));
                updateAll()
                
                // console.log(get_del)
              


            })
            .catch(error => console.error('Ошибка загрузки:', error));
            
    
    }
})








//   Товары


// Функция для получения опций товаров
async function getProductOptionsId(itemId, optionsIdArray) {
    
    try {
        const response = await fetch(`/api/v1/products/${itemId}/`);
        const data = await response.json();

        let res = data.options.filter(option => optionsIdArray.includes(option.id));

        // console.log(res)
        return res

    } catch (error) {
        console.error('Ошибка загрузки опций:', error);
        throw error;
    }
}


async function getComboOptionsId(comboId, optionsIdArray) {
    
    try {
        const response = await fetch(`/api/v1/combos/${comboId}/`);
        const data = await response.json();
        let res = data.items.filter(option => optionsIdArray.includes(option.id));
        return res

    } catch (error) {
        console.error('Ошибка загрузки опций:', error);
        throw error;
    }
}

async function getConstructioOptionsId(constructioId, optionsIdArray) {
    
    try {
        const response = await fetch(`/api/v1/constructors/${constructioId}/`);
        const data = await response.json();

        var res = data.ingredients.filter(option => optionsIdArray.includes(option.id));

        return res
    } catch (error) {
        console.error('Ошибка загрузки опций:', error);
        throw error;
    }
}




// Функция для добавления товара в корзину


async function addToCart(itemId, name, price, image, optionsIdString, type) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};


    setLoyalCart()
    
   
    let optionsIdArray = optionsIdString.split(",").filter(optionId => optionId.trim() !== "").map(optionId => parseInt(optionId.trim(), 10));


    

    let id = itemId;
    let related = false
    if (type === 'product') {
        id += '000';
    } else if (type === 'combo') {
        id += '111';
    } else if (type === 'constructor') {
        id += '222';
    } 
    
    let optionsNameArray = [];
    if (optionsIdArray.length > 0) {
        id += optionsIdArray.join('');
        if (type === 'product') {
            try {
                optionsNameArray = await getProductOptionsId(itemId, optionsIdArray);
                

            } catch (error) {
                console.error('Ошибка при получении настроек продукта:', error);
                // Возможно, здесь нужно предпринять какие-то действия при возникновении ошибки
            }

        } else if (type === 'combo') {
            try {
                optionsNameArray = await getComboOptionsId(itemId, optionsIdArray);
                
            } catch (error) {
                console.error('Ошибка при получении настроек комбо:', error);
                // Возможно, здесь нужно предпринять какие-то действия при возникновении ошибки
            }
        } else if (type === 'constructor') {
            try {
                optionsNameArray = await getConstructioOptionsId(itemId, optionsIdArray);
                
            } catch (error) {
                console.error('Ошибка при получении настроек конструктора:', error);
                // Возможно, здесь нужно предпринять какие-то действия при возникновении ошибки
            }
        }
    }
    // Определите порядковый номер элемента в списке корзины
    let position = Object.keys(cart).length + 1;

    // Добавьте эту позицию в объект itemInfo
    let itemInfo = {
        id: id,
        itemId: itemId,
        type: type,
        name: name,
        price: parseFloat(price),
        image: image,
        quantity: cart[id] ? cart[id].quantity + 1 : 1,
        options: optionsIdArray,
        options_name: optionsNameArray,
        related: related,
        position: position // Добавляем порядковый номер в объект itemInfo
    };
   

    cart[id] = itemInfo;
    localStorage.setItem('cart', JSON.stringify(cart));

    console.log(cart)
    fetchRelatedItems();
    updateAll();
    refreshBalls();
    checkProducts()
    
}


// Пересчитать опции товаров

$(document).on('click', '.cart__item-option', function() {

    if ($(this).hasClass('deactivated')) {
        return
    } else {
        let id = $(this).attr('data-id');
        let price = $(this).attr('data-price');
        let parent = $(this).attr('data-parent');
    
        let cart = JSON.parse(localStorage.getItem('cart')) || {};
        let item = cart[parent];
        let type = item.type;
        let parent_id = item.itemId;
    
        let options = item.options;
        let options_name = item.options_name;
    
        // Найти индекс элемента с заданным id в массивах options и options_name
        let optionIndex = options.indexOf(parseInt(id));
        let optionNameIndex = options_name.findIndex(option => option.id === parseInt(id));
    
        // Удалить элемент из обоих массивов, если найден
        if (optionIndex !== -1 && optionNameIndex !== -1) {
            options.splice(optionIndex, 1);
            options_name.splice(optionNameIndex, 1);
        }
    
        // Преобразовать список options в строку, если это необходимо
        let optionsString = options.join(''); // Преобразовать список options в строку, если это необходимо
    
        let new_id = parent_id
    
        if (type === 'product') {
            new_id += '000';
        } else if (type === 'combo') {
            new_id += '111';
        } else if (type === 'constructor') {
            new_id += '222';
        } 
    
        new_id += optionsString

        let position = cart[parent].position;
    
        item.id = new_id;
        item.position = position;
        item.price -= price;
    
        // Удалить старый элемент из корзины с использованием старого ключа
        delete cart[parent];
    
        // Установить новый ключ для элемента
        let newParent = new_id; // замените на нужный вам ключ
    
        // Добавить элемент в корзину с использованием нового ключа
        if (cart[newParent]) {
            cart[newParent].quantity += 1;
        } else {
            cart[newParent] = item;
        }
        
    
        // Обновить localStorage с обновленными данными корзины
        localStorage.setItem('cart', JSON.stringify(cart));
    
    
        // Обновить отображение корзины и обновить счетчик
        checkProducts();
        updateAll();
        refreshBalls();
        

    }
    
});



// Функция для отображения содержимого корзины
function displayCart() {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};

    // Преобразуем объект корзины в массив
    let cartArray = Object.values(cart);

    // Сортируем массив по значению position
    cartArray.sort((a, b) => a.position - b.position);

    // Преобразуем отсортированный массив обратно в объект
    let sortedCart = {};
    cartArray.forEach(item => {
        sortedCart[item.id] = item;
    });


    let cartItems = document.getElementById('cart-items');
    let cartRelateds = document.getElementById('cart-related');
    
    
    let totalCount = getTotalCount()

    // console.log(sortedCart)

    cartItems.innerHTML = '';
    cartRelateds.innerHTML = '';

    

    if (totalCount === 0) {
        $('.cart__maby').hide()
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
        $('.cart__maby').show()
        
        for (let itemId in sortedCart) {
            let item = cart[itemId];
            
                
            
            if (item.related == false) {

                let cartItem = document.createElement('li');
            

            
                let options_name = item.options_name

                let options_str = ''

                if (options_name) {

                    for (const item of options_name) {

                        
                        let set_remove = false

                        

                        try {
                            // Ваш код здесь
                            if (item.type.option_class !== 'select') {
                                // Если это условие выполняется, будет вызвана ошибка,
                                // если item.type не содержит свойства option_class или не существует
                                set_remove = true;
                            }
                        } catch (error) {
                            // Если произошла ошибка, мы попадаем сюда
                            console.error('Произошла ошибка:', error);
                            // Здесь вы можете вызвать вашу функцию
                            clearCart();
                        }
                        

                        let deactivate_str = ''
                        let remove_btn = ''
                        if (set_remove == false) {
                            deactivate_str = 'deactivated';
                            
                        } else {
                            remove_btn = `
                            <div class="cart__option-remove" data-id="${item.id}">
                                <svg width="26" height="28" viewBox="0 0 26 28" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M5.85522 5.93945L13.1531 14.0505M13.1531 14.0505L20.451 22.1616M13.1531 14.0505L20.451 5.93945M13.1531 14.0505L5.85522 22.1616" stroke="#333333" stroke-width="1.8766" stroke-linecap="round" stroke-linejoin="round"></path>
                                </svg>
                            </div>`
                        }


                        options_str += `
                        <div class="cart__item-option ${deactivate_str}" data-id="${item.id}" data-parent="${itemId}" data-price="${item.option_price}">
                            ${item.option_value}
                            ${remove_btn}
                        
                        </div>`
                    }
                }


                cartItem.innerHTML = `
                    <div class="cart__left" data-position="${item.position}">
                        <div class="cart__left-wrap">

                            <div class="cart__left-img">

                                <img src="${item.image}" alt="${item.name}" style="width: 100px;">
                            </div>
                            <div class="cart__item-info">

                                <span class="cart__item-name">${item.name}</span>

                                <div class="cart__item-options">${options_str}</div>

                            </div>
                        </div>
                    
                        
                    </div>

                    <div class="cart__items-wrap">
                        <div class="cart__btn-wrapper">
                            <button class="cart__plusminus" data-action="minus" data-id="${itemId}">-</button>
                            <div class class="cart__quantity">${item.quantity}</div>
                            <button class="cart__plusminus" data-action="plus" data-id="${itemId}">+</button>
                        </div>
                        <div class="cart__summ">${item.price * item.quantity} ₽</div>
                        <button class="cart__remove" data-id="${itemId}">
                            
                            <?xml version="1.0" encoding="utf-8"?><!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                            <svg width="800px" height="800px" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M20.5001 6H3.5" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                            <path d="M9.5 11L10 16" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                            <path d="M14.5 11L14 16" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                            <path d="M6.5 6C6.55588 6 6.58382 6 6.60915 5.99936C7.43259 5.97849 8.15902 5.45491 8.43922 4.68032C8.44784 4.65649 8.45667 4.62999 8.47434 4.57697L8.57143 4.28571C8.65431 4.03708 8.69575 3.91276 8.75071 3.8072C8.97001 3.38607 9.37574 3.09364 9.84461 3.01877C9.96213 3 10.0932 3 10.3553 3H13.6447C13.9068 3 14.0379 3 14.1554 3.01877C14.6243 3.09364 15.03 3.38607 15.2493 3.8072C15.3043 3.91276 15.3457 4.03708 15.4286 4.28571L15.5257 4.57697C15.5433 4.62992 15.5522 4.65651 15.5608 4.68032C15.841 5.45491 16.5674 5.97849 17.3909 5.99936C17.4162 6 17.4441 6 17.5 6" stroke="#1C274C" stroke-width="1.5"/>
                            <path d="M18.3735 15.3991C18.1965 18.054 18.108 19.3815 17.243 20.1907C16.378 21 15.0476 21 12.3868 21H11.6134C8.9526 21 7.6222 21 6.75719 20.1907C5.89218 19.3815 5.80368 18.054 5.62669 15.3991L5.16675 8.5M18.8334 8.5L18.6334 11.5" stroke="#1C274C" stroke-width="1.5" stroke-linecap="round"/>
                            </svg>
                        </button>
                    </div>
                `;
                
                cartItems.appendChild(cartItem);
                document.getElementById('cart-bottom').style.display = 'block';

            } else {
                let cartRelated = document.createElement('li');
            

            


                cartRelated.innerHTML = `
                    <div class="cart__related-left">

                        <div class="cart__related-left-wrap">
                            <img src="${item.image}" alt="${item.name}" style="width: 50px;height: 50px">

                            
                        </div>
                    
                        
                    </div>

                    <div class="cart__related-wrap">
                        <div class="cart__related-wrapper">
                            <button class="cart__related-plusminus" onclick="minusFromCart(${itemId})">-</button>
                            <div class class="cart__related-quantity">${item.quantity}</div>
                            <button class="cart__related-plusminus" onclick="plusFromCart(${itemId})">+</button>
                        </div>
                        <div class="cart__related-info">

                                <span class="cart__related-name">${item.name}</span>

                                <div class="cart__related-summ">${item.price * item.quantity} ₽</div>

                            </div>
                        
                        
                    </div>
                `;
                
                cartRelateds.appendChild(cartRelated);
                document.getElementById('cart__related-row').style.display = 'block';
                
            }
            

            
            
            
            
        }
    }
    

    // Отображаем общую стоимость и количество товаров
    let totalInfo = document.createElement('li');

    document.getElementById("cart_summ").innerText = getTotalPrice();
    document.getElementById("cart_num").innerText = totalCount;

    // totalInfo.textContent = `Общая стоимость: ${getTotalPrice()}`;

    cartItems.appendChild(totalInfo);

    
    
}


function minusFromCart(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    if (!cart[itemId].related == true) {
        if (cart[itemId].quantity > 1) {

            cart[itemId].quantity--;

        } else {
        
                delete cart[itemId];
            
        }
    } else {

        if (cart[itemId].quantity >= 1) {

            cart[itemId].quantity--;

        } else {
        
                
            
        }

    }

    document.getElementById('cart__related-row').style.display = 'none';
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart__related-row').style.display = 'none';
    updateAll()
    refreshBalls();
    checkProducts()
}

function plusFromCart(itemId) {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    
    cart[itemId].quantity++;
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart__related-row').style.display = 'none';
    updateAll()
    refreshBalls();
    checkProducts()
}

$(document).on('click','.cart__plusminus', function(e) {
    let itemId = $(this).attr('data-id')
    let action = $(this).attr('data-action')

    if (action == 'plus') {

        plusFromCart(itemId)
    } else {
        minusFromCart(itemId)
    }

})

// Функция для удаления товара из корзины
function removeFromCart() {
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    delete cart[itemId];
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart__related-row').style.display = 'none';
    updateAll();
    refreshBalls();
    
}






$(document).on('click','.cart__remove', function(e) {
    let itemId = $(this).attr('data-id')
    let cart = JSON.parse(localStorage.getItem('cart')) || {};
    delete cart[itemId];
    localStorage.setItem('cart', JSON.stringify(cart));
    document.getElementById('cart__related-row').style.display = 'none';
    updateAll()
    refreshBalls();
    checkProducts();
})

// Функция для очистки корзины
function clearCart() {
    localStorage.removeItem('cart');
    
    localStorage.removeItem('order');
    setOrder()
    
    displayCart();
    getTotalCount();

    let order = JSON.parse(localStorage.getItem('order'));

    $('.order__input').each(function() {
        let dataName = $(this).data('name'); // Получаем значение атрибута 'data-name'
        
        // Проверяем, есть ли соответствующее значение в объекте order
        if (order && order[dataName] !== undefined) {
            // Устанавливаем значение в поле ввода
            $(this).val(order[dataName]);
        }
    });
}
// clearCart()


// Сопутствующие товары

function fetchRelatedItems() {
    fetch('/api/v1/related_products/')
        .then(response => response.json())
        .then(data => {
            let cart = JSON.parse(localStorage.getItem('cart')) || {};
            let relatedItems = data.items

            if (relatedItems.length === 0) {
                // Если список сопутствующих товаров пуст, удаляем связанные товары из корзины
                for (let key in cart) {
                    if (cart[key].related) {
                        delete cart[key];
                    }
                }
                localStorage.setItem('cart', JSON.stringify(cart));
                displayCart();
                return; // Завершаем выполнение функции
            }

            relatedItems.forEach(item => {
                let id = item.id
                let itemId = id + '33333'

                if (cart[itemId]) {
                    return;
                } else {
                    let itemInfo = {
                        id: itemId,
                        itemId: id,
                        type: 'related',
                        name: item.name,
                        price: parseFloat(item.price),
                        image: item.image,
                        quantity: 0,
                        options: [],
                        options_name: [],
                        related: true
                    };

                    cart[itemId] = itemInfo;
                    localStorage.setItem('cart', JSON.stringify(cart));
                }
            })

            displayCart();
        })
        .catch(error => console.error('Ошибка загрузки сопутствующих товаров:', error));
}
fetchRelatedItems();










// login register
$(document).on('click', '.order__register-btn' ,function(e){

    let csrf = $('input[name="csrfmiddlewaretoken"]').val()
    let phone = $('.order__input-login').val()
   
    $.ajax({
        method: "POST",
        url: "/accounts/code/",
        data: { 
            csrfmiddlewaretoken: csrf,
            phone: phone
        }
        })
      .done(function( msg ) {

        let innerHTML = `
        <div class="order__register-bottom">
            <input type="text" name="code" class="order__register-input" placeholder="Код подтверждения">
            <button type="button" class="order__register-btn order__register-btn--active">Подтвердить</button>
        </div>
        <br>
        <div class="order__register-bottom">
            <button type="button" class="order__register-btn order__register-btn--resend">Отправить еще раз</button>
        </div>
        `
        $('.order__register-wrapper').html(innerHTML)

        
        $(".order__register-btn--resend").countdown(redirect, 120, "Повторная отправка через ");
        

      });
    
})

$(document).on('keyup', '.order__input-login' ,function(e){
    let phone = $(this).val()
    let min = phone.replace('_', '').replace('-', '').replace('(', '').replace(')', '').replace(' ', '').replace('+', '')
    if (min.length == 13) {
        // $('.user-login__btn').css({'display':'flex'})
        // $(".get-sec").load(location.href + " .get-sec__inner");

        let innerHTML = `
        <div class="order__register-text">
            На номер <span id="login_phone_number">${phone}</span> будет отправлен
            код подтверждения.
        </div>

        <div class="order__register-bottom">
            <button type="button" class="order__register-btn order__register-btn--resend">Отправить</button>
        </div>
        
        `

        $('.order__register-wrapper').html(innerHTML)
        $('.order__register').addClass('order__register--active')

        let secGet = $('.get-sec__inner').attr('data-timer')
        // $('.id_phone-wrap--remove').remove()
        
        if (secGet != '') {
            let sec = 120 - secGet
            let nowData = $('.order__register-btn').text()
            // console.log(sec)
            // console.log(nowData)
            if (sec > 0) {
                if (nowData == 'Подтвердить') {
                    $(".order__register-btn--resendbtn").countdown(redirect, sec, "Повторная отправка через ");
                }
            }
        }

    } else {
        $('.order__register').removeClass('order__register--active')
    }
})


$(document).on('click', '.order__register-btn--active' ,function(e){
    
    let csrf = $('input[name="csrfmiddlewaretoken"]').val()
    let phone = $('.order__input-login').val()
    let code = $('.order__register-input').val()
   
    let shopSettings = JSON.parse(localStorage.getItem('shopSettings'));
    

    $.ajax({
        method: "POST",
        url: "/accounts/register/",
        data: { 
            csrfmiddlewaretoken: csrf,
            phone: phone,
            code: code,
            sms: 'True'
        }
    }).done(function() {

        
        

        // console.log(maxBallsPay())

        getTotalPriceAfterDiscount();

        let order = JSON.parse(localStorage.getItem('order'));
        order.user_phone = phone
        localStorage.setItem('order', JSON.stringify(order));

        
        fetch('/api/v1/get_user/')
            .then(response => response.json())
            .then(data => {
                
                set_data = {
                    'cart_balls': data.cart_balls,
                    'percent_down': data.percent_down,
                    'percent_down_pickup': data.percent_down_pickup,
                    'percent_pay': data.percent_pay,
                    'percent_pay_pickup': data.percent_pay_pickup,
                    'balls_min_summ': data.balls_min_summ,
                    'exclude_combos': data.exclude_combos,
                    'exclude_sales': data.exclude_sales,
                }
                
                localStorage.setItem('loyalCart', JSON.stringify(set_data));
                maxBallsPay();

                console.log(maxBallsPay())
            })
            .catch(error => console.error('Ошибка загрузки пользователя:', error));

        
        
       
        $('.order__input-phone-signup').load(location.href + " .order__input-phone-signup-refresh");
        
        
        var existingElement = $('#balls');
       

        
    }).fail(function() {
        
        $('.order__register-input').addClass('order__register-input--error')
    });

    
})


$(document).on('click', '.order__register-logout' ,function(e){

    $.get("/logout/")
    .done(function(  ) {

        setLoyalCart();
        maxBallsPay();
        // console.log(maxBallsPay())
        $('.order__input-phone-signup').load(location.href + " .order__input-phone-signup-refresh");
        let order = JSON.parse(localStorage.getItem('order'));
        order.user_phone = ''
        order.bonuses_pay = 0;
        localStorage.setItem('order', JSON.stringify(order));
        

        $('.active_balls').remove();
        $('#balls').html('')

        
        getTotalPriceAfterDiscount();
        

    })
    
})



// login register










window.addEventListener('pageshow', function(event) {
    // Проверяем, является ли этот event.persisted событием,
    // что означает, что страница загружается из кэша браузера
    if (event.persisted) {
        // Обновляем состояние LocalStorage до актуального состояния
      
        updateAll()
    }
});



// Обновление всех значений при изменении корзины
function updateAll() {
    
    displayCart();
    getDeliverySumm();
    getTotalPrice();
    getTotalPriceAfterDiscount();
    getTotalCount();

    
    deliveryUpdate()

    
    setLoyalCart()
    getMinimalDelivery()
    getAllDiscount()
    payMethodUpdate()
    maxBallsPay()
    
}









// обработка согласия о принятии Cookies
function setCookiesAccept() {
    let cookies = localStorage.getItem('cookiesAccept');

    

    if (!cookies) {
        let data = {
            'accept_cookies': false
        }
        localStorage.setItem('cookiesAccept', JSON.stringify(data));
    }
}

setCookiesAccept();

function checkCooliesAccept() {
    let cookies = localStorage.getItem('cookiesAccept');

    if (!cookies) {
        return; // Ничего не делаем, если запись о согласии на куки отсутствует
    }

    let cookiesData = JSON.parse(cookies);

    if (cookiesData.accept_cookies !== true) {
        let innerHTML = `
        <div class="cookies">
            <div class="cookies__text">
                Наш сайт использует куки. Продолжая им пользоваться, вы соглашаетесь на обработку 
                персональных данных в соответствии с <a href="/privacy/">политикой конфиденциальности</a>.
            </div>
            <a href="#" class="cookies__button">Согласен</a>
        </div>`;
        $('#for-cookies').html(innerHTML);
    }
}

checkCooliesAccept();

$(document).on('click', '.cookies__button', function(e) {
    e.preventDefault();

    let data = {
        'accept_cookies': true
    };

    localStorage.setItem('cookiesAccept', JSON.stringify(data));
    $('.cookies').remove();
});















var deliveryArea;
var myMap;
ymaps.ready(init);

function init() {

    let city = $('#suggest').attr('data-city')
    let zones = $('#suggest').attr('data-zones')
    let csrf = $('#suggest').attr('data-csrf')
    let flickerAPI = $('#suggest').attr('data-file-zones');
    let datathirdPartyDdelivery = $('#suggest').attr('data-third-party-delivery');

    
    
    if (zones != 'false') {
        
        let suggestView=new ymaps.SuggestView(
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
                    let count = 0
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
                                    hintContent: val.hintContent,
                                    balloonContent: val.balloonContent,
                                    balloonContentHeader: val.balloonContentHeader,
                                   
                                    balloonContentFooter: val.balloonContentFooter
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
                let request = $('#suggest').val();
                // Геокодируем введённые данные.
                ymaps.geocode(request).then(function (res) {
                    let obj = res.geoObjects.get(0),
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
                        
                        let deliveryText = ''
                        myMap.geoObjects.each(function (item) {
                            if(item.geometry.getType() == "Polygon"){
                                if (item.geometry.contains(obj.geometry._coordinates)) {

                                    let suggestElement = $('#suggest');
                                    let headerCartElement = $('#headerCart');
                                    let cartInnerElement = $('.cart__inner');

                                    
                                    if (datathirdPartyDdelivery == 'true') {
                                        
                                        data_del = {
                                            
                                            dotaddress: suggestElement.val(),
                                            csrfmiddlewaretoken: csrf
                                        }

                                        $.post("/delivery/check_price/", data_del, function(response) {
                                            
                                        
                                        })
                                        .done(function( response ) {
                                            // Парсинг JSON-ответа
                                            let price = response.price;
                                            
                                            // console.log(response);
                                            
                                            

                                            let deliveryText = item.properties._data.hintContent
                                            
                                            let deliveryFree = item.properties._data.balloonContentFooter
                                           
                                            let fd=parseInt(deliveryFree.match(/\d+/)[0]);
                                            let min_delivery = item.properties._data.balloonContentFooter.match(/\d+/g)[1];
        
                                            

                                            let data = JSON.parse(localStorage.getItem('deliveryPrice'));
                                            let order = JSON.parse(localStorage.getItem('order'));

                                            data.price_delivery = price
                                            data.free_delivery = fd
                                            

                                            order.address = suggestElement.val()
                                            order.delivery_price = price
        
                                            if(min_delivery) {
                                                let min_delivery_post = parseInt(item.properties._data.balloonContentFooter.match(/\d+/g)[1]);

                                                data.min_delivery = min_delivery_post
                                                $('#suggest').attr('data-min', min_delivery_post)
                                            } 

                                            localStorage.setItem('deliveryPrice', JSON.stringify(data));
                                            localStorage.setItem('order', JSON.stringify(order));


                                            
                                            deliveryUpdate()
                                            $('.show-map').removeClass('order__input--error')
                                        })
                                        

                                    } else {

                                        let deliveryText = item.properties._data.hintContent
                                        let deliveryPrice = item.properties._data.balloonContentBody
                                        let deliveryFree = item.properties._data.balloonContentFooter
                                        let sd=parseInt(deliveryPrice.match(/\d+/)[0]);
                                        let fd=parseInt(deliveryFree.match(/\d+/)[0]);
                                        let min_delivery = item.properties._data.balloonContentFooter.match(/\d+/g)[1];
    
                                        

                                        let data = JSON.parse(localStorage.getItem('deliveryPrice'));
                                        let order = JSON.parse(localStorage.getItem('order'));

                                        data.price_delivery = sd
                                        data.free_delivery = fd
                                        

                                        order.address = suggestElement.val()
                                        order.delivery_price = sd
    
                                        if(min_delivery) {
                                            let min_delivery_post = parseInt(item.properties._data.balloonContentFooter.match(/\d+/g)[1]);

                                            data.min_delivery = min_delivery_post
                                            $('#suggest').attr('data-min', min_delivery_post)
                                        } 

                                        localStorage.setItem('deliveryPrice', JSON.stringify(data));
                                        localStorage.setItem('order', JSON.stringify(order));


                                        
                                        deliveryUpdate()
                                        $('.show-map').removeClass('order__input--error')

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



// Рабочее время


function checkCurrentTime() {
    var d = new Date();
    var currentTime = d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();

    
    let day = d.getDay()

    if (d.getDay() == 0) {
        day = 6
    }

    fetch(`/api/v1/get_work_active/${day}/`)
        .then(response => response.json())
        .then(data => {
            var startDelivery = data.start_delivery;
            var endDelivery = data.end_delivery;
            var startSecondDelivery = data.start_second_delivery;
            var endSecondDelivery = data.end_second_delivery;

            if ((currentTime >= startDelivery && currentTime <= endDelivery) || (currentTime >= startSecondDelivery && currentTime <= endSecondDelivery)) {
                
                // Здесь можно выполнить какие-то действия, если текущее время попадает в один из диапазонов
            } else {

                let workTime = JSON.parse(localStorage.getItem('workTime')) || {};

                

                if (!workTime.is_open) {
                    $('.delivery-popup').removeClass('delivery-popup--active')
                } else {
                    $('.delivery-popup').addClass('delivery-popup--active')
                }

                
                

                
            }
        })
        .catch(error => console.error('Ошибка загрузки рабочего времени:', error));
}

$(document).ready(function() {
    checkCurrentTime();
    let workTime = JSON.parse(localStorage.getItem('workTime'));
    if (!workTime) {
        localStorage.setItem('workTime', JSON.stringify({is_open: true}));
    } 
    


});

$('.delivery-popup__btn').click(function() {
    localStorage.setItem('workTime', JSON.stringify({is_open: false}));
    $('.delivery-popup').removeClass('delivery-popup--active')
})




// Дополнительные товары в корзине
function getCartProduct() {
    fetch('/api/v1/get_cart_products/')
        .then(response => response.json())
        .then(data => {

            for (let i = 0; i < data.length; i++) {
                let item = data[i];
                let itemHtml = `
                    <div class="cart__item">
                        <div class="cart__item-img">
                            <a href="/catalog/${item.id}/">
                                <img src="${item.thumb}" alt="${item.name}">
                            </a>
                        </div>
                        <div class="cart__item-info">
                            <div class="cart__item-name">
                                <a href="/catalog/${item.id}/">
                                    ${item.name}
                                </a>
                            </div>
                            
                        </div>
                        <div class="cart__item-price">
                            ${parseFloat(item.price).toFixed(2)}₽
                        </div>
                    </div>
                `;
                console.log(itemHtml)
            }
        })
        .catch(error => console.error('Ошибка загрузки товаров:', error));
}

// getCartProduct()
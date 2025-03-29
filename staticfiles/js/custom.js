(function ($) {
  "use strict";

  function Click_menu_hover() {
    if ($(".tab-demo").length) {
      $.fn.tab = function (options) {
        var opts = $.extend({}, $.fn.tab.defaults, options);
        return this.each(function () {
          var obj = $(this);

          $(obj)
            .find(".tabHeader li")
            .on(opts.trigger_event_type, function () {
              $(obj).find(".tabHeader li").removeClass("active");
              $(this).addClass("active");

              $(obj).find(".tabContent .tab-pane").removeClass("active show");
              $(obj)
                .find(".tabContent .tab-pane")
                .eq($(this).index())
                .addClass("active show");
            });
        });
      };
      $.fn.tab.defaults = {
        trigger_event_type: "click", //mouseover | click é»˜è®¤æ˜¯click
      };
    }
  }

  Click_menu_hover();

  function Tab_menu_activator() {
    if ($(".tab-demo").length) {
      $(".tab-demo").tab({
        trigger_event_type: "mouseover",
      });
    }
  }

  Tab_menu_activator();

  //*============ background color js ==============*/
  $("[data-bg-color]").each(function () {
    var bg_color = $(this).data("bg-color");
    $(this).css({
      "background-color": bg_color,
    });
  });

  //*============ background image js ==============*/
  $("[data-bg-image]").each(function () {
    var bg = $(this).data("bg-image");
    $(this).css({
      background: "no-repeat center 0/cover url(" + bg + ")",
    });
  });

  if ($(".chapter-tab").length) {
    var triggerChapterTabList = [].slice.call(
      document.querySelectorAll(".chapter-tab .nav-link")
    );
    triggerChapterTabList.forEach(function (triggerEl) {
      var tabTrigger = new bootstrap.Tab(triggerEl);

      triggerEl.addEventListener("click", function (event) {
        $(".chapter-tab").find(".active").removeClass("active");
        event.preventDefault();
        tabTrigger.show();
      });
    });
  }

  $(".ar_top").on("click", function () {
    var getID = $(this).next().attr("id");
    var result = document.getElementById(getID);
    var qty = result.value;
    $(".proceed_to_checkout .update-cart").removeAttr("disabled");
    if (!isNaN(qty)) {
      result.value++;
    } else {
      return false;
    }
  });

  $(".ar_down").on("click", function () {
    var getID = $(this).prev().attr("id");
    var result = document.getElementById(getID);
    var qty = result.value;
    $(".proceed_to_checkout .update-cart").removeAttr("disabled");
    if (!isNaN(qty) && qty > 0) {
      result.value--;
    } else {
      return false;
    }
  });

  //parallax js

  if ($(".banner_animation_01").length > 0) {
    $(".banner_animation_01").parallax({
      scalarX: 10.0,
      scalarY: 0.0,
    });
  }
  if ($(".banner_animation_02").length > 0) {
    $(".banner_animation_02").parallax({
      scalarX: 10.0,
      scalarY: 4.0,
    });
  }
  if ($(".banner_animation_03").length > 0) {
    $(".banner_animation_03").parallax({
      scalarX: 7.0,
      scalarY: 10.0,
    });
  }

  /*===========Portfolio isotope js===========*/
  function portfolioMasonry() {
    var pr_portfolio = $("#project_portfolio");
    if (pr_portfolio.length) {
      pr_portfolio.imagesLoaded(function () {
        pr_portfolio.isotope({
          itemSelector: ".projects_item",
          layoutMode: "masonry",
          transformsEnabled: true,
          transitionDuration: "700ms",
        });

        // Add isotope click function
        $("#portfolio_filter div").on("click", function () {
          $("#portfolio_filter div").removeClass("active");
          $(this).addClass("active");

          var selector = $(this).attr("data-filter");
          pr_portfolio.isotope({
            filter: selector,
            animationOptions: {
              animationDuration: 750,
              easing: "linear",
              queue: false,
            },
          });
          return false;
        });
      });
    }
  }
  portfolioMasonry();

  /*====== slider js ======*/
  if ($(".slick_slider").length) {
    $(".slick_slider").slick({});
  }
  $(document).ready(function () {
    if ($(".slick_slider_tab").length) {
      $(".slick_slider_tab").slick({
        infinite: true,
        slidesToShow: 2,
        slidesToScroll: 1,
        responsive: [
          {
            breakpoint: 1199,
            settings: {
              slidesToShow: 2,
            },
          },
          {
            breakpoint: 767,
            settings: {
              slidesToShow: 1,
            },
          },
        ],
      });
    }
    if ($(".best_slider").length) {
      $(".best_slider").slick({
        infinite: true,
        slidesToShow: 4,
        slidesToScroll: 1,
        responsive: [
          {
            breakpoint: 1199,
            settings: {
              slidesToShow: 3,
            },
          },
          {
            breakpoint: 991,
            settings: {
              slidesToShow: 2,
            },
          },
          {
            breakpoint: 767,
            settings: {
              slidesToShow: 1,
            },
          },
        ],
      });
    }

    if ($(".testimonial_slider_three").length) {
      $(".testimonial_slider_three").slick({
        dots: true,
        arrows: false,
        slidesToShow: 3,
        slidesToScroll: 1,
        infinite: true,
        loop: true,
        centerMode: true,
        centerPadding: "0px",
        responsive: true,
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 3,
              centerMode: true,
              centerPadding: "0px",
            },
          },
          {
            breakpoint: 991,
            settings: {
              slidesToShow: 2,
              centerMode: false,
            },
          },
          {
            breakpoint: 767,
            settings: {
              slidesToShow: 1,
              centerMode: false,
            },
          },
        ],
      });
    }
  });

  $('a[data-bs-toggle="pill"]').on("shown.bs.tab", function (e) {
    if ($(".slick_slider_tab,.best_slider,.slick_slider_author").length) {
      $(".slick_slider_tab,.best_slider,.slick_slider_author").slick(
        "setPosition"
      );
    }
  });

  //counter up js
  if ($(".counter").length) {
    $(".counter").counterUp({
      delay: 10,
      time: 1000,
    });
  }

  if ($("#slider-range").length) {
    var $slider = $("#slider-range");
    //Get min and max values
    var priceMin = $slider.attr("data-price-min"),
      priceMax = $slider.attr("data-price-max");

    //Set min and max values where relevant
    $("#price-filter-min, #price-filter-max").map(function () {
      $(this).attr({
        min: priceMin,
        max: priceMax,
      });
    });
    $("#price-filter-min").attr({
      placeholder: "min " + priceMin,
      value: priceMin,
    });
    $("#price-filter-max").attr({
      placeholder: "max " + priceMax,
      value: priceMax,
    });

    $slider.slider({
      range: true,
      min: Math.max(priceMin, 0),
      max: priceMax,
      values: [priceMin, priceMax],
      slide: function (event, ui) {
        // $("#amount").val("$" + ui.values[0] + " - $" + ui.values[1]);
        $("#price-filter-min").val(ui.values[0]);
        $("#price-filter-max").val(ui.values[1]);
      },
    });

    $("#price-filter-min, #price-filter-max").map(function () {
      $(this).on("input", function () {
        updateSlider();
      });
    });
    function updateSlider() {
      $slider.slider("values", [
        $("#price-filter-min").val(),
        $("#price-filter-max").val(),
      ]);
    }
  }

  if ($(".selectpickers").length > 0) {
    $(".selectpickers").niceSelect();
  }

  if ($(".bsSelectpicker").length > 0) {
    $(".bsSelectpicker").bsSelect({
      search: false,
    });
  }

  var $window = $(window);
  var didScroll,
    lastScrollTop = 0,
    delta = 5,
    $mainNav = $("#header"),
    $mainNavHeight = $mainNav.outerHeight(),
    scrollTop;

  $window.on("scroll", function () {
    didScroll = true;
    scrollTop = $(this).scrollTop();
  });

  setInterval(function () {
    if (didScroll) {
      hasScrolled();
      didScroll = false;
    }
  }, 200);

  function hasScrolled() {
    if (Math.abs(lastScrollTop - scrollTop) <= delta) {
      return;
    }
    if (scrollTop > lastScrollTop && scrollTop > $mainNavHeight) {
      $mainNav.css("top", -$mainNavHeight);
    } else {
      if (scrollTop + $(window).height() < $(document).height()) {
        $mainNav.css("top", 0);
      }
    }
    lastScrollTop = scrollTop;
  }

  // === Back to Top Button
  var back_top_btn = $("#back-to-top");

  $(window).scroll(function () {
    if ($(window).scrollTop() > 300) {
      back_top_btn.addClass("show");
    } else {
      back_top_btn.removeClass("show");
    }
  });

  back_top_btn.on("click", function (e) {
    e.preventDefault();
    $("html, body").animate({ scrollTop: 0 }, "300");
  });

  //sticky header
  function navbarFixed() {
    if ($("#header").length) {
      $(window).scroll(function () {
        var scroll = $(window).scrollTop();
        if (scroll) {
          $("#header").addClass("fixed-header");
        } else {
          $("#header").removeClass("fixed-header");
        }
      });
    }
  }
  navbarFixed();

  /*  Menu Click js  */
  function Menu_js() {
    if ($(".submenu").length) {
      $(".submenu > a").click(function () {
        var location = $(this).attr("href");
        window.location.href = location;
        return false;
      });
    }
  }
  Menu_js();

  /*--------------- mobile dropdown js--------*/
  if ($(window).width() < 991) {
    function active_dropdown2() {
      $("li.submenu > a").after(
        '<span class="ti-angle-down mobile_dropdown_icon"/>'
      );
      $(".menu > li .mobile_dropdown_icon").on("click", function () {
        $(this).parent().find("> ul").first().slideToggle(300);
        $(this).parent().siblings().find("> ul").hide(300);
        return false;
      });
    }
    active_dropdown2();
  }

  if ($(".mySwiper").length) {
    var swiper = new Swiper(".mySwiper", {
      pagination: {
        el: ".swiper-pagination",
        type: "progressbar",
      },
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
    });
  }

  if ($(".flip_btn").length) {
    $(".flip_btn").on("click", function (e) {
      e.preventDefault();
      $(".bj_book_img").toggleClass("flip");
    });
  }

  if ($(".search").length) {
    $(".search a").on("click", function () {
      if ($(this).parent().hasClass("open")) {
        $(this).parent().removeClass("open");
      } else {
        $(this).parent().addClass("open");
        setTimeout(function () {
          $(".menu-search-form .form-control").focus();
        }, 500);
      }

      return false;
    });
  }

  if ($(".gallerypdf").length) {
    $(".gallerypdf").fancybox({
      openEffect: "elastic",
      closeEffect: "elastic",
      autoSize: true,
      type: "iframe",
      iframe: {
        preload: false, // fixes issue with iframe and IE
      },
    });
  }

  /*--------- WOW js-----------*/

  function bodyScrollAnimation() {
    var scrollAnimate = $("body").data("scroll-animation");
    if (scrollAnimate === true) {
      new WOW({}).init();
    }
  }
  bodyScrollAnimation();

  // Function to update quantity
  function updateQuantity($input, change) {
    let newValue = parseInt($input.val()) + change;
    // Ensure the new value is within the min and max range
    newValue = Math.max(
      parseInt($input.attr("min")),
      Math.min(parseInt($input.attr("max")), newValue)
    );
    $input.val(newValue);
  }

  // Event handler for minus button
  $(".cart_quantity .quantity_btn.minus").on("click", function () {
    var $input = $(this).siblings('input[type="number"]');
    updateQuantity($input, -1);
  });

  // Event handler for plus button
  $(".cart_quantity .quantity_btn.plus").on("click", function () {
    var $input = $(this).siblings('input[type="number"]');
    updateQuantity($input, +1);
  });

  // Event handler for manual input
  $('.cart_quantity input[type="number"]').on("change", function () {
    updateQuantity($(this), 0); // This will ensure the value stays within range
  });

  $(".toggle-password").click(function () {
    $(this).toggleClass("fa-eye fa-eye-slash");
    var input = $($(this).attr("data-toggleTarget"));
    if (input.attr("type") == "password") {
      input.attr("type", "text");
    } else {
      input.attr("type", "password");
    }
  });

  $(".addres_sidebar_cart_trigger").on("click", function () {
    $(".side_menu").addClass("menu-opened");
    $("body").removeClass("menu-is-closed").addClass("menu-is-opened");
  });

  $(".close_nav,.close_sidebar").on("click", function (e) {
    if ($(".side_menu").hasClass("menu-opened")) {
      $(".side_menu").removeClass("menu-opened");
      $("body").removeClass("menu-is-opened");
    } else {
      $(".side_menu").addClass("menu-opened");
    }
  });

  $(".click_capture").on("click", function () {
    $("body").removeClass("menu-is-opened").addClass("menu-is-closed");
    $(".side_menu").removeClass("menu-opened");
  });

  $("#track_view_more_btn").on("click", function (e) {
    e.preventDefault();
    $(this).css("display", "none");
    $(".single_track_step.second_step,.single_track_step.first_step").css(
      "display",
      "flex"
    );
  });

  $(".dynamic-star-rating i").click(function () {
    const rating = $(this).index() + 1;
    $(".dynamic-star-rating-input").val(rating);
    $(".dynamic-star-rating i").removeClass("active");
    $(this).prevAll().addBack().addClass("active");

    if ($(".dynamic-rating-text").length) {
      $(".dynamic-rating-text").show();
    }
  });

  // Event: when total_select_box checkbox is clicked
  $("#cart_total_select_check").on("change", function () {
    const isChecked = $(this).is(":checked");
    $(".cart_item_select .form-check-input").prop("checked", isChecked);
  });

  // Event: when any cart_item_select .form-check-input checkbox changes
  $(".cart_item_select .form-check-input").on("change", function () {
    if (
      $(".cart_item_select .form-check-input:checked").length ===
      $(".cart_item_select .form-check-input").length
    ) {
      // If all check_one checkboxes are checked, check#cart_total_select_check
      $("#cart_total_select_check").prop("checked", true);
    } else {
      // If any check_one checkbox is unchecked, uncheck#cart_total_select_check
      $("#cart_total_select_check").prop("checked", false);
    }
  });

  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Global function for tab arrow controls
  function initTabArrowControls(tabGroupId) {
    const $tabList = $(`#${tabGroupId}.nav-pills`);
    const $tabs = $tabList.find(".nav-link");
    const $prevArrow = $(".prev-tab");
    const $nextArrow = $(".next-tab");

    function updateArrowState() {
      const $activeTab = $tabs.filter(".active");
      $prevArrow.prop("disabled", $activeTab.is(":first-child"));
      $nextArrow.prop("disabled", $activeTab.is(":last-child"));
    }

    function switchTab(direction) {
      const $activeTab = $tabs.filter(".active");

      let $targetTab;
      if (direction === "next") {
        $targetTab = $activeTab.next(".nav-link");
      } else {
        $targetTab = $activeTab.prev(".nav-link");
      }

      if ($targetTab.length) {
        $targetTab.tab("show");
        updateArrowState();
      }
    }

    $prevArrow.on("click", () => switchTab("prev"));
    $nextArrow.on("click", () => switchTab("next"));

    // Update arrow state on tab change
    $('a[data-bs-toggle="pill"]').on("shown.bs.tab", updateArrowState);

    // Initial arrow state
    updateArrowState();
  }

  // Initialize the tab arrow controls

  initTabArrowControls("pills-tab-two");

  function copyWithJquery() {
    var parentDiv = $(".copy_number_widget");
    parentDiv.find(".actn_btn").click(function () {
      var temp = $("<input>");
      $("body").append(temp);
      temp.val(parentDiv.find(".target").text()).select();
      document.execCommand("copy");
      temp.remove();
      $(this).text("Copied");
      setTimeout(function (item) {
        parentDiv.find(".actn_btn").text("Copy");
      }, 4000);
    });
  }
  copyWithJquery();

  function activateTabByHash() {
    var hash = window.location.hash;
    if (hash) {
      var tabId = hash + "-tab"; // Add '-tab' to match the tab id
      var $tab = $(tabId);

      if ($tab.length) {
        // Activate the tab
        var tabTrigger = new bootstrap.Tab($tab[0]);
        tabTrigger.show();

        // Add a small delay to ensure the tab content is visible
        setTimeout(function () {
          // Smooth scroll to the tab content
          $("html, body").animate(
            {
              scrollTop: $(hash).offset().top,
            },
            300
          ); // 800ms for smooth scroll effect
        }, 300); // 100ms delay to ensure content visibility
      }
    }
  }

  // Run on page load
  activateTabByHash();

  // Update tab when hash changes
  $(window).on("hashchange", function () {
    activateTabByHash();
  });

  $('a[href="#product_review"]').click(function () {
    activateTabByHash();
  });
})(jQuery);

// Automated Cart System
function automatedAddToCartSystem() {
  function generateProductKey() {
    return "PK-" + Math.random().toString(36).substr(2, 9).toUpperCase();
  }

  $(".add-to-cart-automated").each(function () {
    const productKey = generateProductKey();
    $(this).attr("data-product-key", productKey);
    $(this).addClass(productKey);
  });

  var shoppingCart = (function () {
    cart = [];
    function Item(img, name, price, count, mrp, productKey) {
      this.img = img;
      this.name = name;
      this.price = price;
      this.count = count;
      this.mrp = mrp;
      this.productKey = productKey;
    }
    var y = JSON.parse(localStorage.getItem("shoppingCart"));
    for (var item in y) {
      if (y[item].productKey) {
        $("." + y[item].productKey).text("Added To Cart");
        $("." + y[item].productKey).prop("disabled", true);
      }
    }

    // Save cart
    function saveCart() {
      localStorage.setItem("shoppingCart", JSON.stringify(cart));
      var x = JSON.parse(localStorage.getItem("shoppingCart"));
      for (var item in x) {
        $("." + x[item].productKey).text("Added To Cart");
        $("." + x[item].productKey).prop("disabled", true);
      }
    }

    // Load cart
    function loadCart() {
      cart = JSON.parse(localStorage.getItem("shoppingCart"));
    }
    if (localStorage.getItem("shoppingCart") != null) {
      loadCart();
    }

    var obj = {};

    // Add to cart
    obj.addItemToCart = function (img, name, price, count, mrp, productKey) {
      for (var item in cart) {
        if (cart[item].productKey === productKey) {
          cart[item].count++;
          $("." + cart[item].productKey).text("Added To Cart");
          $("." + cart[item].productKey).prop("disabled", true);
          saveCart();
          showToast(); // Call the toast function
          return;
        }
      }
      var item = new Item(img, name, price, count, mrp, productKey);
      cart.push(item);
      saveCart();
      showToast(); // Call the toast function
    };

    // Set count from item
    obj.setCountForItem = function (productKey, count) {
      for (var i in cart) {
        if (cart[i].productKey === productKey) {
          cart[i].count = count;
          break;
        }
      }
    };

    // Remove item from cart
    obj.removeItemFromCart = function (productKey) {
      for (var item in cart) {
        if (cart[item].productKey === productKey) {
          cart[item].count--;
          if (cart[item].count === 0) {
            cart.splice(item, 1);
          }
          break;
        }
      }
      saveCart();
    };

    // Remove all items from cart
    obj.removeItemFromCartAll = function (productKey) {
      for (var item in cart) {
        if (cart[item].productKey === productKey) {
          $("." + cart[item].productKey).text("Add To Cart");
          $("." + cart[item].productKey).prop("disabled", false);
          cart.splice(item, 1);
          break;
        }
      }
      saveCart();
    };

    // Clear cart
    obj.clearCart = function () {
      cart = [];
      $(".add-to-cart-automated").text("Add To Cart");
      saveCart();
    };

    // Count cart
    obj.totalCount = function () {
      var totalCount = 0;
      for (var item in cart) {
        totalCount += cart[item].count;
      }
      return totalCount;
    };

    // Total cart
    obj.totalCart = function () {
      var totalCart = 0;
      for (var item in cart) {
        totalCart += cart[item].price * cart[item].count;
      }
      return Number(totalCart.toFixed(2));
    };

    // List cart
    obj.listCart = function () {
      var cartCopy = [];
      for (i in cart) {
        item = cart[i];
        itemCopy = {};
        for (p in item) {
          itemCopy[p] = item[p];
        }
        itemCopy.total = Number(item.price * item.count).toFixed(2);
        cartCopy.push(itemCopy);
      }
      return cartCopy;
    };
    return obj;
  })();

  $(".add-to-cart-automated").click(function (event) {
    event.preventDefault();
    var img = $(this).data("img");
    var name = $(this).data("name");
    var price = Number($(this).data("price"));
    var mrp = Number($(this).data("mrp"));
    var productKey = $(this).data("product-key");
    shoppingCart.addItemToCart(img, name, price, 1, mrp, productKey);
    displayCart();
  });

  // Clear items
  $(".clear-cart").click(function () {
    shoppingCart.clearCart();
    displayCart();
    $(".add-to-cart-automated").text("Add To Cart");
    $(".add-to-cart-automated").prop("disabled", false);
  });

  function displayCart() {
    var cartArray = shoppingCart.listCart();
    var output = "";
    for (var i in cartArray) {
      output +=
        "<li class='cart-single-item clearfix'>" +
        "<div class='cart-img'>" +
        "<img src=" +
        cartArray[i].img +
        "></div>" +
        "<div class='cart-content text-left'>" +
        "<p class='cart-title'><a href='product-single.html'>" +
        cartArray[i].name +
        "</a></p>" +
        "<p>" +
        (cartArray[i].mrp ? "<del>$" + cartArray[i].mrp + "</del> - " : "") +
        "$" +
        cartArray[i].price +
        "</p>" +
        "</div>" +
        "<button class=' cart-remove action delete-item' data-product-key=" +
        cartArray[i].productKey +
        "><span class='ti-close'></span></button>" +
        "</li>";
    }

    $(".cart-dropdown").html(output);
    $(".total-cart-amount").html(shoppingCart.totalCart());
    $(".total-cart-count").html(shoppingCart.totalCount());
  }

  // Function to show the toast
  function showToast() {
    var toastEl = document.getElementById("cartToast");
    var toast = new bootstrap.Toast(toastEl);
    toast.show();
  }

  // Delete item button
  $(".cart-dropdown").on("click", ".delete-item", function (event) {
    var productKey = $(this).data("product-key");
    shoppingCart.removeItemFromCartAll(productKey);
    displayCart();
  });

  // -1
  $(".cart-dropdown").on("click", ".minus-item", function (event) {
    var productKey = $(this).data("product-key");
    shoppingCart.removeItemFromCart(productKey);
    displayCart();
  });

  // +1
  $(".cart-dropdown").on("click", ".plus-item", function (event) {
    var img = $(this).data("img");
    var productKey = $(this).data("product-key");
    shoppingCart.addItemToCart(img, productKey);
    displayCart();
  });

  // Item count input
  $(".cart-dropdown").on("change", ".item-count", function (event) {
    var productKey = $(this).data("product-key");
    var count = Number($(this).val());
    shoppingCart.setCountForItem(productKey, count);
    displayCart();
  });

  displayCart();
}

// Call the function
automatedAddToCartSystem();

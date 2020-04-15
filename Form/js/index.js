var checkout = {

    el: {
        // Inputs
        cardNumberInput: $('[id^="card-number"]'),
        cardHolderNameInput: $("#card-holder-name"),
        cardExpInput: $('[id^="card-exp"]'),
        cardExpMonthInput: $("#card-exp-month"),
        cardExpYearInput: $("#card-exp-year"),
        cardCCVInput: $("#card-ccv"),
        // Containers
        cardNumberContainer: $(".card__number"),
        cardHolderNameContainer: $(".card__holder-name"),
        cardExpContainer: $(".card__exp"),
        cardCCVContainer: $(".card__ccv"),
        // Flip
        flip: $(".flip"),
        flipFront: $(".flip__front"),
        flipBack: $(".flip__back")
    },
    // Main init
    init: function() {
        checkout.bindUIActions();
    },
    // Binding UI actions
    bindUIActions: function() {
        checkout.el.cardNumberInput.on("keyup", checkout.displayCardNumber);
        checkout.el.cardHolderNameInput.on("keyup", checkout.displayCardName);
        checkout.el.cardExpInput.on("change", checkout.displayCardExp);
        checkout.el.cardCCVInput.on("keyup", checkout.displayCardCCV);
        checkout.el.cardCCVInput.on("focus", checkout.flipCard);
        checkout.el.cardCCVInput.on("blur", checkout.resetFlip);
    },
    // Displaying card number
    displayCardNumber: function() {
        var cardNumber = "";
        // Building the credit card number 
        checkout.el.cardNumberInput.each(function() {
            cardNumber += $(this).val() + ' ';
        });
        // Auto-focus next input if character count is greater than 3
        $(this).val().length > 3 ?
            $(this).next().focus() : false;
        // Auto-focus previous input if character count is 0
        $(this).val() == "" ?
            $(this).prev().focus() : false;
        // Displaying credit card number
        checkout.el.cardNumberContainer.html(cardNumber);
    },
    // Displaying card name
    displayCardName: function() {
        checkout.el.cardHolderNameContainer.html(checkout.el.cardHolderNameInput.val());
    },
    // Displaying expiration date
    displayCardExp: function() {
        // Displaying nothing if both date fields are empty
        if (checkout.el.cardExpMonthInput.val() === "" && checkout.el.cardExpYearInput.val() === "") {
            checkout.el.cardExpContainer.html("");
        } else {            
            checkout.el.cardExpContainer.html(checkout.el.cardExpMonthInput.val() + "/" + checkout.el.cardExpYearInput.val());
        }
    },
    // Displaying card ccv
    displayCardCCV: function() {
        checkout.el.cardCCVContainer.html(checkout.el.cardCCVInput.val());
    },
    // Showing back of the card
    flipCard: function() {
        checkout.el.flip.css("transform", "rotateY(180deg)");
        checkout.el.flipFront.removeClass("shown");
        checkout.el.flipBack.addClass("shown");
    },
    // Showing front of the card
    resetFlip: function() {
        checkout.el.flip.removeAttr("style");
        checkout.el.flipBack.removeClass("shown");
        checkout.el.flipFront.addClass("shown");
    }
};

checkout.init();
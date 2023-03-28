
function adjustMainBgHeight() {
    var imgWidth = 1200;
    var imgHeight = 200;
    var img = $('.tm-main-bg');
    var currentWidth = img.width();
    var currentHeight = (currentWidth * imgHeight) / imgWidth;
    
    img.css('height', currentHeight);
}


function checkInput(elementId)  {
  var inputElement = document.getElementById(elementId);
  if (isNaN(inputElement.value)) {
      alert("Please enter a number for the element number.");
      inputElement.value = "";
  }
}

function showRemoveSuccess() {
  document.getElementById("remove-success").style.display = "block";
}

function toggleAddForm() {
  var addForm = document.getElementById("add-form");
  var removeForm = document.getElementById("remove-form");

  if (addForm.style.display === "none") {
      addForm.style.display = "block";
      removeForm.style.display = "none";
  } else {
      addForm.style.display = "none";
  }
}


function toggleRemoveForm() {
  var removeForm = document.getElementById("remove-form");
  var addForm = document.getElementById("add-form");

  // Hide add form if it's visible
  if (addForm.style.display === "block") {
      addForm.style.display = "none";
  }

  // Toggle visibility of remove form
  if (removeForm.style.display === "none") {
      removeForm.style.display = "block";
  } else {
      removeForm.style.display = "none";
  }
}

$(document).ready(function(){
    adjustMainBgHeight();

    $("#add-form").submit(function(event) {
      event.preventDefault(); // Prevent form submission from refreshing the page
      var elementNumber = $("#add_element_number").val();
      var elementName = $("#element_name").val();
      var elementCode = $("#element_code").val();
      var Color1 = $("#color1").val();
      var Color2 = $("#color2").val();
      var Color3 = $("#color3").val();
      var Radius = $("#radius").val();
      $.ajax({
        type: "POST",
        url: "/template/addelement",
        data: { 
                element_number: elementNumber,
                element_name: elementName,
                element_code: elementCode,
                color1: Color1,
                color2: Color2,
                color3: Color3,
                radius: Radius
              },
        success: function(response) {
          $("#add-form").hide(); // Hide the form
          $("#success-message").show(); // Show the success message
        }
      });
    });

    $("#remove-form").submit(function(event) {
      event.preventDefault(); // Prevent form submission from refreshing the page
      var elementNumber = $("#remove_element_number").val();
      $.ajax({
        type: "POST",
        url: "/template/removeelement",
        data: { element_number: elementNumber },
        success: function(response) {
          $("#remove-form").hide(); // Hide the form
          $("#success-message").show(); // Show the success message
        }
      });
    });

    $(window).resize(function() {
        adjustMainBgHeight();
    });
    
    // Mobile menu
    $('.tm-mobile-menu').click(function() {
      $('.tm-nav').toggleClass('show');
    });
    
    if($('.tm-carousel').length) {
      // Carousel
      $('.tm-carousel').slick({
        dots: true,
        infinite: false,
        speed: 300,
        slidesToShow: 4,
        slidesToScroll: 2,
        responsive: [
          {
            breakpoint: 992,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 550,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1
            }
          },
          {
            breakpoint: 420,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1
            }
          }
        ]
      });   
    }  
});
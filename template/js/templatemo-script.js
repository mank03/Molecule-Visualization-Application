
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

function checkNameInput(elementId)  {
  var inputElement = document.getElementById(elementId);
  if (!isNaN(inputElement.value)) {
      alert("Please enter a valid name.");
      inputElement.value = "";
  }
}

// function showRemoveSuccess() {
//   document.getElementById("remove-success").style.display = "block";
// }

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

function showRotatedSvg(moleculeName) {
  var svgContainer = document.getElementById("svg-container");
  svgContainer.innerHTML = "<img src='" + moleculeName + "_rotated.svg' />";
}

function showRotatedSvg(moleculeName) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (this.readyState === 4 && this.status === 200) {
      // When the response is received, set the SVG data as the innerHTML of the svg-container element
      document.getElementById("svg-container").innerHTML = this.responseText;
    }
  };
  xhr.open("GET", "/getMoleculeRotatedSVG/" + encodeURIComponent(moleculeName), true);
  xhr.send();
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
          // $("#add-form").hide(); // Hide the form
          document.getElementById('success-message').textContent = `Successfully added ${elementName}`;
          $("#success-message").show(); // Show the success message
          // alert("Element added successfully"); // Show an alert
          console.log("Element added successfully.");
        },
        error: function(xhr, textStatus, errorThrown) {
          // $("#add-form").hide(); // Hide the form
          alert("This element name, number, or code already exists! Please refer to the table below."); // Show an alert
          console.log("Error adding element:", errorThrown);
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
          // $("#remove-form").hide(); // Hide the form
          document.getElementById('success-message2').textContent = `Successfully removed Element ${elementNumber}`;
          $("#success-message2").show(); // Show the success message
          // alert("Element removed successfully"); // Show an alert
          console.log("Element removed successfully.");
        },
        error: function(xhr, textStatus, errorThrown) {
          // $("#remove-form").hide(); // Hide the form
          alert("Element number does not exist! Please refer to the table below."); // Show an alert
          console.log("Error removing element:", errorThrown);
        }
      });
    });


    $("#upload-form").submit(function(event) {
      event.preventDefault(); // Prevent form submission from refreshing the page
    
      // Get the form data
      var formData = new FormData($(this)[0]);
    
      $.ajax({
        url: "/template/molecule",
        type: "POST",
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
          // Hide the form
          $("#upload-form").hide();
          // Show the success message
          $("#success-message").show();
        },
        error: function(xhr, status, error){
          alert("Error uploading file. Ensure SDF file is valid and required elements are uploaded."); // Show an alert
          console.log(xhr.responseText);
        }
      });
    });

    // CHANGE FROM FORM TO ROTATE-FORM, UPDATE THE ROTATE FORM IN HTML FILE TO MATCH ID
    $("#rotate-form").submit(function(event) {
      event.preventDefault(); // Prevent form submission from refreshing the page
      // Get the form data
      var x = $("#x-coordinate").val();
      var y = $("#y-coordinate").val();
      var z = $("#z-coordinate").val();
      var selectedElement = $("#selected-element").text();
      $("input[name='element_name']").val(selectedElement);
      $.ajax({
        url: "/template/rotate",
        type: "POST",
        data: { 
          xVal: x,
          yVal: y,
          zVal: z,
          element: selectedElement,
        },
        success: function(response) {
          showRotatedSvg(selectedElement);
          // Hide the form
          // $("form").hide();
          // Show the success message
          // $("#success-message").show();
        },
        error: function(xhr, status, error) {
          // Handle errors here
          console.log(xhr.responseText);
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
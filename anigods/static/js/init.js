/***HELPER FUNCTIONS***/

function getParameterByName(name, url) {
  if (!url) url = window.location.href;
  name = name.replace(/[\[\]]/g, '\\$&');
  var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
    results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}


/***MATERIAL COMPONENTS INITIALIZE***/
document.addEventListener('DOMContentLoaded', function () {

  //init mobile menu
  var elems = document.querySelectorAll('.sidenav');
  var navInstances = M.Sidenav.init(elems);

  //init chapter selection 

  var elems = document.querySelectorAll('select');
  var instances = M.FormSelect.init(elems);


  //  init modal
  var modals = document.querySelectorAll('.modal');
  var modalInstances = M.Modal.init(modals);

  //init tabs
  var el = document.querySelector('.tabs');
  var tabInstance = M.Tabs.init(el);

  //init slider
  var elems = document.querySelectorAll('.slider');
  var instances = M.Slider.init(elems);

  //fetch data for autocomplete
  var autoComplete = document.querySelectorAll('.autocomplete');
  if (autoComplete) {
    fetch('/api/autocomplete/')
      .then((resp) => resp.json()) // Transform the data into json
      .then(
        function (data) {
          window.acInstances = M.Autocomplete.init(autoComplete, {
            data: data,
            limit: 6,
            minLength: 1,
            onAutocomplete: function (option) { location = data[option] }
          });
        }

      ).catch(function (err) {
        console.log('Fetch Error:', err);
      });
  }


});


/***CUSTOM CODE***/

(function ($) {

  $(document).ready(function () {

    if ($(".owl-carousel")) {
      $(".owl-carousel").owlCarousel({
        items: 3,
        loop: true,
        margin: 20,
        lazyLoad: true,
        autoplay:true,
        sautoplayTimeout:5000,
        autoplayHoverPause:true,
        responsive: {
          0: {
            items: 1,
          },
          1200  : {
            items: 2
          },
          1576: {
            items: 3
          }
        }
      });
    }


    //remove loader after 300ms
    setTimeout(function () {
      $('.progress').remove();
    }, 300);
  });

  $(".dropdown-trigger").dropdown();

  //show search bar on icon clicked
  $('.icon-search').click(function (e) {
    e.preventDefault();
    $(this.getAttribute('id-target')).toggleClass('show');
  });


  //add target _blank to external link
  $('a:not(.breadcrumb)').each(function () {
    if (this.href.split('/')[2] !== window.location.host && this.target !== "_blank") {
      this.target = "_blank";
    }
  });

  //add links to chapter select boxes
  $select = $('select.project-child-select');
  if ($select) {
    $select.on('change', function () {
      var url = window.location.href.split('/').slice(0, 6);
      url.push($(this).val());
      window.location = url.join('/');

    });
  }


  //disable next and prev button
  var nextOption = $('select.project-child-select').first().find('option[selected]').next().val();
  if (!nextOption) {
    $('.project-child-next a').addClass('disabled');
  } else {
    $('.project-child-next a').click(function (e) {
      e.preventDefault();
      var url = window.location.href.split('/').slice(0, 6);
      url.push(nextOption);
      window.location = url.join('/');
    })
  }

  var prevOption = $('select.project-child-select').first().find('option[selected]').prev().val();
  if (!prevOption) {
    $('.project-child-prev a').addClass('disabled');
  } else {
    $('.project-child-prev a').click(function (e) {
      e.preventDefault();
      var url = window.location.href.split('/').slice(0, 6);
      url.push(prevOption);
      window.location = url.join('/');
    })
  }

  //control avatar field
  function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('#imagePreview').css('background-image', 'url('+e.target.result +')');
            $('#imagePreview').hide();
            $('#imagePreview').fadeIn(650);
        }
        reader.readAsDataURL(input.files[0]);
    }
  }
  $("#imageUpload").change(function() { readURL(this); });


  //edit field when clicked on pencil icon
  $('.username-field i.fas.fa-pencil-alt').click(function() {
    $this = $(this);
    $this.addClass('focus');
    $inputField = $this.siblings('input');
    $inputField.removeAttr('disabled').focus();
    $('.username-note').show();
    $inputField.blur(function(){
        $inputField.attr('disabled','disabled');
        $this.removeClass('focus');
        $('.username-note').hide();
    })
});

})(jQuery);



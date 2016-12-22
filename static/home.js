$(function() {
  // input of the original image
  $('.submit-original[type="file"]').on('change', function() {
    // grab file directly, blob / file thing
    // window.Object(e.target.value);
  });
  $('.submit-original[type="text"]').on('change', function(e) {
    // image on remote website
    $('img.original').attr('src', e.target.value);
  });

  // paint-over palettes from 'voices' app, which was cool
  $('.colorable').map(function(c, colorable) {
    // add the UI to each palette
    var red = $('<li>').append('<span class="color red highlight">_</span>');
    var green = $('<li>').append('<span class="color green">_</span>');
    var blue = $('<li>').append('<span class="color blue">_</span>');
    $(colorable).find('.color-palette').append(red);
    $(colorable).find('.color-palette').append(green);
    $(colorable).find('.color-palette').append(blue);
    
    var colorctx = $(colorable).find('canvas')[0].getContext('2d');
    colorctx.fillStyle = 'red';
    colorctx.strokeStyle = 'red';
    colorctx.lineWidth = 8;
    if (window.devicePixelRatio && window.devicePixelRatio > 1) {
      colorctx.lineWidth = 12;
    }
    
    $(colorable).find('.color').click(function(e) {
      $(".color").removeClass("highlight");
      $(e.currentTarget).addClass("highlight");
      colorctx.strokeStyle = $(e.currentTarget).css('color');
      colorctx.fillStyle = $(e.currentTarget).css('color');
    });
  
    // add painting code here
    var writing = false;
    var lastPt = null;
    var areas = false;
    
    $(colorable).find('canvas').on('mousedown', function() {
      writing = true;
      lastPt = null;
      if (!areas) {
        colorctx.beginPath();
      }
    })
    .on('mouseup mouseout', function() {
      writing = false;
    })
    .on('mousemove', function(e) {
      if (writing && !areas) {
        if (lastPt) {
          colorctx.lineTo(e.offsetX, e.offsetY);
          colorctx.stroke();
        }
        colorctx.moveTo(e.offsetX, e.offsetY);
        lastPt = [e.offsetX, e.offsetY];
      }
    });
  });

  // offer the test case (no need for custom images)
  $('.test-case').click(function() {
    // download /test-case, paste into canvases
    $('img.original').attr('src', '/test-case/image.jpg');
    
    var ctxOld = $('#old-regions')[0].getContext('2d');
    var imgOld = new Image();
    imgOld.onload = function() {
      ctxOld.drawImage(imgOld, 0, 0);
      $('#old-regions').css({
        marginTop: (-1 * imgOld.height) + 'px',
        opacity: 0.5
      });
      $('img.original').css({
        height: imgOld.height,
        width: imgOld.width,
        marginBottom: '-15px'
      });
    };
    imgOld.src = '/test-case/image-mask.jpg';
    
    var ctxNew = $('#new-regions')[0].getContext('2d');
    var imgNew = new Image();
    imgNew.onload = function() {
      ctxNew.drawImage(imgNew, 0, 0);
    };
    imgNew.src = '/test-case/image-mask-new.jpg';    
    
    // user must click run themselves
  });
  
  // if everything goes well, user clicks this to start
  $('.run').click(composeAndSubmitForm);
  
  function composeAndSubmitForm() {
    var originalImage = $('img.original').attr('src');
    var origImg = new Image();
    origImg.onload = function() {
      $('input[name="original"]').val();
      
      $('input[name="mask"]').val();
      
      $('input[name="new-mask"]').val();
      
      $('form').submit();
    };
    origImg.src = originalImage;
  }
  
});
var page = require('webpage').create();
sleep(20)
page.onResourceReceived = function(res) {
  if (res.stage === 'end') {
    if (res.status == '500'){
      console.error('Internal server error');
      phantom.exit(1)
    }
    console.log('Status code: ' + res.status);
  }
};

page.open('http://127.0.0.1:5309', function() {
  phantom.exit();
});

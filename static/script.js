function load() {
    document.getElementById("promptDisplay").enabled = false;
}

function submitForm() {
    // Get values from form
    var form = document.getElementById('socialMediaForm');
    var twitterHandle = document.getElementById('twitter').value;
    var linkedinHandle = document.getElementById('linkedin').value;
    var mbtiIndicator = document.getElementById('MBTI').value;
  
    // Check if any field is empty
    if (!twitterHandle || !linkedinHandle || !mbtiIndicator) {
      alert('Please fill in all fields.');
      return; // Stop form submission
    }
  
    // If all fields are filled, proceed with form submission
    // You can add additional logic here if needed
    // alert('Form submitted!');
    
    var formData = {
        twitter: twitterHandle,
        linkedin: linkedinHandle,
        MBTI: mbtiIndicator
      };


    document.getElementById('submitButton').enabled = false;

    fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    }).then(response => response.json()).then(object => {
        console.log(object.message);
        document.getElementById("promptDisplay").innerHTML   = object.message;
    });

    twitterHandle.value = '';
    linkedinHandle.value = '';
    mbtiIndicator.value = '';

    document.getElementById('submitButton').enabled = true;

  }
   
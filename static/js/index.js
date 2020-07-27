$(document).ready(function() {
	// ------------------------------------------ Toggle chatbot -----------------------------------------------
	$('.profile_div').click(function() {
		$('.profile_div').toggle();
		$('.chatCont').toggle();
		$('.bot_profile').toggle();
		$('.chatForm').toggle();
		document.getElementById('chat-input').focus();
	});

	$('.close').click(function() {
		$('.profile_div').toggle();
		$('.chatCont').toggle();
		$('.bot_profile').toggle();
		$('.chatForm').toggle();
	});

	// on input/text enter--------------------------------------------------------------------------------------
	$('#chat-input').on('keyup keypress', function(e) {
		var m = 'Fideria_Friday';
		console.log(m);
		var keyCode = e.keyCode || e.which;
		var text = $("#chat-input").val();
		if (keyCode === 13) {
			if(text == "" ||  $.trim(text) == '') {
				e.preventDefault();
				return false;
			} else {
				$("#chat-input").blur();
				setUserResponse(text);				
				send(text);
				e.preventDefault();
				return false;
			}
		}
	});
	
	// on input/text enter--------------------------------------------------------------------------------------
	$('#support_group').on('keyup keypress', function(e) {
		console.log(m);
		var keyCode = e.keyCode || e.which;
		var text = $("#support_group").val();
		if (keyCode === 13) {
			if(text == "" ||  $.trim(text) == '') {
				e.preventDefault();
				return false;
			} else {			
				change_page(text);
				e.preventDefault();
				return false;
			}
		}
	});
	
	
	//------------------------------------------- Render New Page request to Chatbot Python ---------------------------------------
	function change_page(usrl) {
		$.ajax({
			url: usrl,
			type: "GET",
			data: "userId=12345&userName=test",
			success: function(data) {				
				alert('successful');
			},
			error: function(e) {
				console.log (e);
			}
		});
	}

	//------------------------------------------- Send request to Chatbot Python ---------------------------------------
	function send(text) {		
		var sen = {'human':text}
		$.ajax({
			url: "/pass_val/",
			type: "POST",
			data: JSON.stringify(sen),
			contentType:'application/json;charset=UTF-8',
			success: function(rsp) {				
				var reply = rsp.reply;				
				playSound(rsp.play);
				updateImage(rsp.sentiment)
				
				var replies = rsp.reply;
			    var replyLength = rsp.reply.length;
				
				for(i=0;i<replyLength;i++) {
					
					if (replies[i] == "Do you want to hear a joke?"){						
						addJokes();
					}else if(replies[i] == "Covid"){
						addFacts();
					}else{
						main(replies[i]);
					}
				}
			},
			error: function(e) {
				console.log (e);
			}
		});
	}
	
	var imgs = {};
	imgs[0] = "/static/img/default-01.png";
	imgs[1] = "/static/img/happy1-01.png";
	imgs[2] = "/static/img/happy2-01.png";
	imgs[3] = "/static/img/happy3-01.png";
	imgs[-1]= "/static/img/sad1-01.png";
	imgs[-2]= "/static/img/sad2-01.png";
	imgs[-3]= "/static/img/sad3-01.png";
	
	function updateImage(val) {	    
	    userSentiment = 0
		if(val == "Sad") {
			userSentiment = -3
	    }
	    if(val == "Happy" ) {
			userSentiment = 3
	    }
	    document.getElementById('main-image').src = imgs[userSentiment];
	}
	
	function playSound(val) {
		var a = new Audio("/static/img/reply_"+ val+".mp3");
		a.play();
	}

	function jsonp_callback(json){
		alert(json.reply);
	}

	//------------------------------------------- Main function ------------------------------------------------
	function main(speech) {
		var m = 'Fideria Changed';
		console.log(m);
		console.log(speech);
		playSound()
		setBotResponse(speech);
	}


	//------------------------------------ Set bot response in result_div -------------------------------------
	function setBotResponse(val) {
		setTimeout(function(){
			var BotResponse = '<p class="botResult">'+val+'</p><div class="clearfix"></div>';
			$(BotResponse).appendTo('#result_div');
			scrollToBottomOfResults();
			hideSpinner();
		}, 500);
	}


	//------------------------------------- Set user response in result_div ------------------------------------
	function setUserResponse(val) {
		var UserResponse = '<p class="userEnteredText">'+val+'</p><div class="clearfix"></div>';
		$(UserResponse).appendTo('#result_div');
		$("#chat-input").val('');
		scrollToBottomOfResults();
		showSpinner();
		$('.suggestion').remove();
	}


	//---------------------------------- Scroll to the bottom of the results div -------------------------------
	function scrollToBottomOfResults() {
		var terminalResultsDiv = document.getElementById('result_div');
		terminalResultsDiv.scrollTop = terminalResultsDiv.scrollHeight;
	}


	//---------------------------------------- Ascii Spinner ---------------------------------------------------
	function showSpinner() {
		$('.spinner').show();
	}
	function hideSpinner() {
		$('.spinner').hide();
	}

	//------------------------------------------- Jokes --------------------------------------------------
	function addJokes() {
		main("Do you want to hear a joke?");
		setTimeout(function() {
			$('<p class="suggestion"></p>').appendTo('#result_div');
			$('<div class="sugg-title">Choice: </div>').appendTo('.suggestion');			
			$('<span class="sugg-options"> YES</span>').appendTo('.suggestion');
			$('<span class="sugg-options"> NO</span>').appendTo('.suggestion');
			scrollToBottomOfResults();
		}, 1000);
	}
		
	//------------------------------------------- Facts & Symptoms--------------------------------------------------
	function addFacts() {
		setTimeout(function() {
			$('<p class="suggestion"></p>').appendTo('#result_div');
			$('<div class="sugg-title">Covid Facts: </div>').appendTo('.suggestion');			
			$('<span class="sugg-options"> <ol><li>Clean your hands often. Use soap and water, or an alcohol-based hand rub.</li><li>Maintain a safe distance from anyone who is coughing or sneezing.</li><li>Don’t touch your eyes, nose or mouth.</li><li>Cover your nose and mouth with your bent elbow or a tissue when you cough or sneeze.</li><li>Stay home if you feel unwell.</li><li>If you have a fever, a cough, and difficulty breathing, seek medical attention. Call in advance.</li><li>Follow the directions of your local health authority.</li></ol>  </span>').appendTo('.suggestion');
			$('<div class="sugg-title">Covid Symptoms: </div>').appendTo('.suggestion');			
			$('<span class="sugg-options"> <ul><li>Fever</li><li>Tiredness</li><li>Dry Cough.</li><li>Aches and Pains</li><li>Nasal Congestion</li><li>Sore Throat</li><li>Diarrhoea</li></ul>  </span>').appendTo('.suggestion');
			scrollToBottomOfResults();
		}, 1000);
	}
	
	//------------------------------------------- Image -----------------------------------------------------------
	function addImage() {
		setTimeout(function() {
			$('<p class="suggestion"></p>').appendTo('#result_div');
			$('<div class="sugg-title">Covid Symptoms: </div>').appendTo('.suggestion');			
			scrollToBottomOfResults();
		}, 1000);
	}
	
	//------------------------------------------- Suggestions --------------------------------------------------
	function addSuggestion(textToAdd) {
		setTimeout(function() {
			var suggestions = "Hello"
			$('<p class="suggestion"></p>').appendTo('#result_div');
			$('<div class="sugg-title">Suggestions: </div>').appendTo('.suggestion');
			// Loop through suggestions
			for(i=0;i<1;i++) {
				$('<span class="sugg-options">'+suggestions+'</span>').appendTo('.suggestion');
			}
			scrollToBottomOfResults();
		}, 1000);
	}

	// on click of suggestions get value and send to API.AI
	$(document).on("click", ".suggestion span", function() {
		console.log(text);
		var text = this.innerText;
		setUserResponse(text);
		send(text);
		$('.suggestion').remove();
	});
	// Suggestions end -----------------------------------------------------------------------------------------
});

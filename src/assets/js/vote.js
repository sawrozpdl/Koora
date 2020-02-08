import Voter from './voter.js';


let voteForms = document.getElementsByClassName('vote-form');
let voteCounts = document.getElementsByClassName('vote-count');
let upvoteButtons = document.getElementsByClassName('upvote-button');
let downvoteButtons = document.getElementsByClassName('downvote-button');


for (let count = 0 ;count < voteForms.length; count++ ) {

  let voter = new Voter({
    voteForm : voteForms[count],
    voteCount : voteCounts[count],
    upvoteButton : upvoteButtons[count],
    downvoteButton : downvoteButtons[count]
  })

  voter.listen()
} 
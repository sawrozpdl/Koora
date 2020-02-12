import request from './request.js';

class Voter {
  
    constructor(config) {

        this.vote = null;

        if (config) {
            this.voteForm = config.voteForm;
            this.voteCount = config.voteCount;
            this.upvoteButton = config.upvoteButton;
            this.downvoteButton = config.downvoteButton;
        }
    }

    _handleError = error => $(`#${this.voteCount.id}`).notify('Please log in to vote', 'error');

    _disableVoting = () => {
        this.upvoteButton.disabled = true;
        this.downvoteButton.disabled = true;
    };

    _enableVoting = () => {
        this.upvoteButton.disabled = false;
        this.downvoteButton.disabled = false;
    };

    _upvoteClientSide = () => {
        this.upvoteButton.classList.toggle('active');
        this.downvoteButton.classList.remove('active');
    };

    _downvoteClientSide = () => {
        this.downvoteButton.classList.toggle('active');
        this.upvoteButton.classList.remove('active');
    };

    _updateClientSide = ({ vote_count }) => {
        this.voteCount.innerHTML = vote_count;
        return this.vote === 'up' ? this._upvoteClientSide() : this._downvoteClientSide();
    };

    listen = () => {
      
        this.upvoteButton.onclick = () => (this.vote = 'up');

        this.downvoteButton.onclick = () => (this.vote = 'down');

        this.voteForm.onsubmit = event => {

            event.preventDefault();

            const { object_id, model_name, csrfmiddlewaretoken, access_token } = event.target;

            let url = event.target.action;

            let data = {
                object_id: object_id.value,
                model_name: model_name.value,
                vote_type: this.vote,
            };

            let csrf_token = csrfmiddlewaretoken.value;

            let token = access_token.value;

            let headers = {
                'X-CSRFToken': csrf_token,
                'Content-Type': 'application/json',
                'Token': token,
            };

            this._disableVoting();

            request(url, data, headers, 'POST')
                .then(response => this._updateClientSide(response))
                .catch(error => this._handleError(error))
                .finally(() => this._enableVoting());
        };
    };
}

export default Voter;

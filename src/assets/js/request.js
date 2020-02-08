const request = (url, data, headers, method="GET") => {
        
  return new Promise((resolve, reject) => {

      let request = new XMLHttpRequest();
      request.open(method, url, true);


      for (let key in headers) {
          request.setRequestHeader(key, headers[key])
      }

      request.onload = function() {
          let response = JSON.parse(this.response);
          if (response.status === 200)
              return resolve(response)
          reject(response)
      }

      request.send(JSON.stringify(data));  
  })
}

export default request
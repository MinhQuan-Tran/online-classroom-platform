<template>
    <div>
      <div class="input-box">
        <input type="text" :placeholder="placeholder" ref="autocompleteInput" />
      </div>
    </div>
  </template>
  
  <script>
  export default {

    data() {
        return {
            placeholder: "Enter your address here.",
            currentTimeout: null,
            currentPromiseReject: null,
            MIN_ADDRESS_LENGTH: 3,
            DEBOUNCE_DELAY: 300,
        }
      
    },
    watch: {
        currentValue: "handleInput", 
    },
    methods: {
        handleInput(newVal){
            if (this.currentTimeout){
                clearTimeout(this.currentTimeout);
            }

            if (this.currentPromiseReject){
                this.currentPromiseReject({
                    canceled: true,
                })
            }

            if (!newVal || newVal.length < this.MIN_ADDRESS_LENGTH){
                return false;
            }

            this.currentTimeout = setTimeout(() => {
                this.currentTimeout = null;

                const apiKey = "ed5fb372406848eaa8ca7b9a3a6690a9";

                const url = `https://api.geoapify.com/v1/geocode/autocomplete?text=${encodeURIComponent(
                    newVal
                )}&format=json&limit=5&apiKey=${apiKey}`;
            })
        },

      addressAutocomplete() {
        // Access the input element using $refs
        const inputElement = this.$refs.autocompleteInput;
        inputElement.addEventListener("input", this.handleInput);

       
        
        function handleSelectedOption(data){
            console.log("Selected option: " + data);
        }

        function addressAutocomplete(containerElement, callback, options) {
        // Create container for input element
            const inputContainerElement = document.createElement("div");
            inputContainerElement.setAttribute("class", "input-container");
            containerElement.appendChild(inputContainerElement);

            // Create input element
            const inputElement = document.createElement("input");
            inputElement.setAttribute("type", "text");
            inputElement.setAttribute("placeholder", options.placeholder);
            inputContainerElement.appendChild(inputElement);

        // Add event listener for user selection and invoke the callback
            inputElement.addEventListener("input", function () {
            // Simulate address autocomplete logic
            const autoCompleteData = [
                "Address 1",
                "Address 2",
                "Address 3",
            ]; // Replace with actual autocomplete data

            // Invoke the callback function with the selected option
            const selectedOption = autoCompleteData.find(
                (option) => option === inputElement.value
            );
            if (selectedOption) {
                callback(selectedOption);
            }
            });
        }

        addressAutocomplete(document.getElementById('autocomplete-container'), (data) => {
            console.log("selectedOption: " + data);
        }, {
            placeholder: "Enter an address here"
        }) 

      },
    },
  };
  </script>
  
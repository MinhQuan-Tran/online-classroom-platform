<script>
//import AddressAutocomplete from '../components/AddressAutocomplete.vue';
export default{
    /*
    components: {
        AddressAutocomplete,
    },
    */
    data(){
        return{
            placeholder: "Enter an address here",
            courseId: 2, //Define which course to get info from here
            teachersName: "",
            courseFee: 0,
            formData:{
                isOnline: false,
                description:'',
                address:'',
                phoneNumber:''
            },
            maxCharacters: 200
        }
    },
    computed: {
        computedIsOnline: {
            get() {
                return this.formData.isOnline ? "true" : "false";
            },
            set(value){
                this.formData.isOnline = value === "true" ? true : value === "false" ? false: null;
            }
        }
    },
    methods:{
        submitApplyInfo(event){
            event.preventDefault();
            // jump page (path "apply-course?course_id=1")
            //sets the html element '$refs.submitBtn' to processing
            //does it through the variable 'data-status'
            this.$refs.submitBtn.setAttribute("data-status", "processing");
            //we then disable it so the user cannot click the button again WHILE its processing
            this.$refs.submitBtn.disabled = true;
            this.$refs.submitBtn.innerText = "processing...";
            
            fetch(`${import.meta.env.VITE_ROOT_API}/apply_course`, {
                method: "POST", //POST means we are SENDING data to the server
                credentials: "include", //includes credentials such as cookies, important for authentication
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.$cookies.get('csrf_token'),
                },
                body: JSON.stringify(this.formData) //the body property is what we are sending

            }) 
            .then(response => {
                //after we send the request through fetch, it gives us a Promise.
                //in Javascript, Promise is an object that represents the eventual completion or failure of an
                //asynchronous operation and the resulting value.
                if (!response.ok){
                    return response.json().then(data => {
                        throw new Error(data.message);
                    });
                }
                console.log(response);
                return response.json();
            })
            .then(data => {
                console.log(data);
                
            })
            .catch(error => {
                console.error(error);
            });       
        },
        getCourseInformation(){
            fetch(`${import.meta.env.VITE_ROOT_API}/apply_course?course_id=${this.courseId}` , {
                method: "GET",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": this.$cookies.get('csrf_token'),
                }
            }).then(response => {
                if (!response.ok){
                    return response.json().then(data => {
                        throw new Error(data.message);
                    });
                }
                return response.json();
            })
            .then(data => {
                this.teachersName = data.name;
                this.courseFee = data.fee
                console.log(data);
            })
            .catch(error => {
                console.error(error)
            })
        },
        isTextboxLimitReached() {
            if(this.formData.description.length > this.maxCharacters){
                this.formData.description = this.formData.description.substring(0, this.maxCharacters);
            }
            const isLimitReached = this.formData.description.length >= this.maxCharacters
            return isLimitReached
        }
    },
    watch: {
        'formData.isOnline'(newVal){
            console.log('formData.isOnline changed to: ', newVal);
        }  
    },
    created() {
        this.getCourseInformation();
    }
};

</script>

<template>
    <main>
        <div class="flex-container">
            <div class="column bioCardColumn">
                <img src="@/assets/profile-picture.jpg" alt="">
                <h2>{{ teachersName }}</h2>
                <h3>${{ courseFee }}/hr</h3>
            </div>
            <form class="column fieldsColumn" @submit="submitApplyInfo">
                <div class="field-flex-container">
                    <p></p>
                    <label for="description-box" style="position: relative; right: 1px;">Additional Information ({{ this.maxCharacters - this.formData.description.length }} Characters Remaining)</label>
                    
                    <div>
                        <textarea name="description" id="description" v-model="formData.description" @input="isTextboxLimitReached()" cols="41" rows="10"></textarea>
                    </div>
                    
                    <div class="online-toggle">
                        <input id="toggle-on" class="toggle toggle-left" name="toggle" v-model= "computedIsOnline" value="false" type="radio" checked>
                        <label for="toggle-on" class="btn_left">In-Person</label>

                        <input id="toggle-off" class="toggle toggle-right" name="toggle" v-model="computedIsOnline" value="true" type="radio">
                        <label for="toggle-off" class="btn_right">Online</label>
                    </div>
                    
                    <div v-if="!formData.isOnline">
                        <!--<AddressAutocomplete :placeholder="placeholder" />-->
                        <div class="input-box">
                            <input type="text" name="address" id="address" placeholder="" v-model="formData.address" required>
                            <label for="address">Address</label>
                        </div>
                        
                    </div>
                    
                    <div class="input-box">
                        <input type="text" name="phoneNumber" id="phoneNumber" placeholder="" v-model="formData.phoneNumber" required
                        pattern="[0-9]{10}">
                        <label for="phoneNumber">Phone Number</label>
                    </div>                    

                </div>
                <!--The apply button might need to only redirect the student straight to payment.
                Payment page should get the user id of the current user and course, and the course rate and payment method
                Then create a new entry in Payment model in models.py-->>
                <button class="submit-button" ref="submitBtn" type="submit" data-status="normal">Apply</button>
            </form>
        </div>
    </main>
</template>

<style scoped>
.autocomplete-container{
    margin-bottom: 0px;
}

.input-container {
    display: flex;
}

.input-container input{
    flex: 1;
    outline: none;
    border: 1px solid rgba(0,0,0,0.2);
    padding: 10px;
    padding-right: 31px;
    font-size: 16px;
}

body,html{
    background: #efefef;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100%;
    z-index: -1;
}

.btn_right{
    border: 3px solid gray;
    display: inline-block;
    padding: 10px;
    position: relative;
    text-align: center;
    transition: background 600ms ease, color 600ms ease;
    border-top-right-radius: 12px;
    border-bottom-right-radius: 12px;
}

.btn_left {
    border: 3px solid gray;
    display: inline-block;
    padding: 10px;
    position: relative;
    text-align: center;
    transition: background 600ms ease, color 600ms ease;
    border-top-left-radius: 12px;
    border-bottom-left-radius: 12px;
    left: -5.5px;
    
}

/* Reference: https://codepen.io/magnificode/pen/ojYJJP */
input[type="radio"].toggle {
    display: none; /*Renders the original text of the radio button invisible, replacing it with each label instead */
    & + label{
        cursor: pointer;
        min-width: 175px;
        left: 0px;
        &:not(:checked):hover{
            background: none;
            /* None for now, need to figure out how to only apply hover effect only when
                unchecked. Color: lightgoldenrodyellow;*/
            color: none;
        }
        &:after{
            background: lightyellow;
            content: "";
            height: 99.5%;
            position: absolute;
            top: 0;
            transition: left 250ms cubic-bezier(0.77, 0, 0.175, 1);
            width: 98.8%;
            z-index: -1;
        }
    }
    &.toggle-left + label {
        border-right: 0;
        &:after{
            left: 100%
        }
    }
    &.toggle-right + label{
        margin-left: -5px;
        &:after{
            left: -99%;
        }
    }
    &:checked + label {
        cursor: default;
        color: black;
        transition: color 200ms;
        
        &:after{
            left: 0;
        }
    }
}

.flex-container{
    display: flex;
    justify-content: center;
    margin-top: 5em;
    
}

.field-flex-container{
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.column {
    padding: 20px;
    margin: 10px;
    text-align: center;
    font-size: 18px;
}

.bioCardColumn {
    width: 200px;
    background-color: none;
    color: #f1f1f1;
    min-width: 15em;
    margin-right: 80px;
    transform: translateY(54px);
}

.bioCardColumn img {
    max-width: 100%;
    max-height: 100%;
    display: block;
    margin: 0 auto;
}

.fieldsColumn {
    width: 400px;
    color: #f1f1f1;
    min-width: 15em;
}

#description {
    resize: none;
    border: none;
    border-radius: 8px;
    font-family: Arial, Helvetica, sans-serif;
    font-size: large;

}

#description :focus{
    border-radius: 20px;
    
}

</style>

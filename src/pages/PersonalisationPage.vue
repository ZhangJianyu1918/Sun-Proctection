<template>
    <div class="suggestion-container">
      <h1 class="title">
        <font-awesome-icon icon="sun" /> Personalised Suggestion
      </h1>
      <div class="divider"></div>
  
      <div class="form-content">
        <div class="form-section">
          <div class="form-group">
            <label for="gender">
              <font-awesome-icon icon="user" /> Gender
            </label>
            <select id="gender" v-model="formData.gender" class="form-select">
              <option disabled value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="non-binary">Non-binary</option>
              <option value="other">Other</option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="skinType">
              <font-awesome-icon icon="palette" /> Skin Type
            </label>
            <select id="skinType" v-model="formData.skinType" class="form-select">
              <option disabled value="">Select skin type</option>
              <option value="normal">Normal</option>
              <option value="dry">Dry</option>
              <option value="oily">Oily</option>
              <option value="combination">Combination</option>
              <option value="sensitive">Sensitive</option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="skinTone">
              <font-awesome-icon icon="paint-brush" /> Skin Tone
            </label>
            <select id="skinTone" v-model="formData.skinTone" class="form-select">
              <option disabled value="">Select skin tone</option>
              <option value="fair">Fair</option>
              <option value="light">Light</option>
              <option value="medium">Medium</option>
              <option value="olive">Olive</option>
              <option value="tan">Tan</option>
              <option value="deep">Deep</option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="sunscreenUsage">
              <font-awesome-icon icon="umbrella-beach" /> Sunscreen Usage
            </label>
            <select id="sunscreenUsage" v-model="formData.sunscreenUsage" class="form-select">
              <option disabled value="">Select frequency of sunscreen usage</option>
              <option value="daily">Daily</option>
              <option value="often">Often</option>
              <option value="sometimes">Sometimes</option>
              <option value="rarely">Rarely</option>
              <option value="never">Never</option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="sunExposure">
              <font-awesome-icon icon="sun" /> Sun Exposure
            </label>
            <select id="sunExposure" v-model="formData.sunExposure" class="form-select">
              <option disabled value="">Select frequency of sun exposure</option>
              <option value="minimal">Minimal (indoors most of the time)</option>
              <option value="low">Low (brief periods outdoors)</option>
              <option value="moderate">Moderate (1-3 hours outdoors daily)</option>
              <option value="high">High (4+ hours outdoors daily)</option>
              <option value="extreme">Extreme (outdoor occupation)</option>
            </select>
          </div>
  
          <div class="button-container">
            <button @click="saveChanges" class="save-button">
              <font-awesome-icon icon="save" /> Save Change
            </button>
          </div>
        </div>
  
        <div class="recommendation-section">
          <h2 class="recommendation-title">
            <font-awesome-icon icon="lightbulb" /> Recommendation
          </h2>
          <div class="recommendation-content" v-if="recommendation">
            <p>{{ recommendation }}</p>
            <div class="form-group reminder-time-group">
              <label for="reminderTime">
                <font-awesome-icon icon="clock" /> Set Reminder Time
              </label>
              <div class="time-input-container">
                <input
                  type="number"
                  id="reminderTime"
                  v-model.number="formData.reminderTime"
                  class="form-input time-input"
                  min="1"
                  placeholder="Enter time"
                >
                <select v-model="formData.timeUnit" class="form-select time-unit">
                  <option value="minutes">Minutes</option>
                  <option value="seconds">Seconds</option>
                </select>
              </div>
            </div>
          </div>
          <div class="recommendation-content" v-else>
            <p>Please fill out the form to receive a personalised recommendation.</p>
          </div>
          <div class="button-container">
            <button
              v-if="recommendation"
              @click="setReminder"
              class="reminder-button"
              :disabled="formData.reminderTime <= 0 || !recommendation"
            >
              <font-awesome-icon icon="bell" /> Set Reminder
            </button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PersonalisedSuggestion',
    data() {
      return {
        formData: {
          gender: '',
          skinType: '',
          skinTone: '',
          sunscreenUsage: '',
          sunExposure: '',
          reminderTime: 0,
          timeUnit: 'minutes',
        },
        recommendation: '',
        reminderTimeout: null,
      };
    },
    methods: {
      saveChanges() {
        this.generateRecommendation();
      },
      generateRecommendation() {
        if (!this.validateForm()) {
          alert('Please fill out all fields to receive a recommendation.');
          return;
        }
  
        let rec = `Hello, based on your profile: `;
        rec += `Your skin type is ${this.formData.skinType}, and your skin tone is ${this.formData.skinTone}. `;
  
        if (this.formData.sunExposure === 'high' || this.formData.sunExposure === 'extreme') {
          rec += `Given your high sun exposure, we strongly recommend daily application of SPF 50+ sunscreen and wearing protective clothing.`;
        } else {
          rec += `We recommend a balanced skincare routine and using SPF protection regularly.`;
        }
  
        if (this.formData.sunExposure === 'high' || this.formData.sunExposure === 'extreme') {
          rec += ` Don't forget to wear protective clothing like hats and long sleeves to minimize sun exposure.`;
        }
        if (this.formData.sunscreenUsage === 'rarely' || this.formData.sunscreenUsage === 'never') {
          rec += ` Consider making sunscreen a daily habit to protect your skin from harmful UV rays.`;
        }
  
        this.recommendation = rec;
      },
      validateForm() {
        for (const key in this.formData) {
          if (key !== 'reminderTime' && key !== 'timeUnit' && this.formData[key] === '') {
            return false;
          }
        }
        return true;
      },
      setReminder() {
        if (this.reminderTimeout) {
          clearTimeout(this.reminderTimeout);
        }
  
        const delay = this.formData.timeUnit === 'seconds'
          ? this.formData.reminderTime * 1000
          : this.formData.reminderTime * 60 * 1000;
  
        this.reminderTimeout = setTimeout(() => {
          alert(`Reminder: ${this.recommendation}`);
        }, delay);
  
        alert(`Reminder set for ${this.formData.reminderTime} ${this.formData.timeUnit}!`);
      },
    },
    beforeUnmount() {
      if (this.reminderTimeout) {
        clearTimeout(this.reminderTimeout);
      }
    },
  };
  </script>
  
  <style scoped>
  .suggestion-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
  
  .title {
    text-align: center;
    font-size: 36px;
    color: #4840b7;
    margin-bottom: 20px;
    flex-shrink: 0;
  }
  
  .divider {
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 30px;
    flex-shrink: 0;
  }
  
  .form-content {
    display: flex;
    gap: 20px;
    flex: 1;
    overflow: hidden;
  }
  
  .form-section {
    flex: 1;
    padding-right: 20px;
    border-right: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  .recommendation-section {
    flex: 1;
    padding-left: 20px;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }
  
  .form-group {
    margin-bottom: 20px;
    flex-shrink: 0;
  }
  
  .reminder-time-group {
    margin-top: 20px;
    margin-bottom: 10px;
    flex-shrink: 0;
  }
  
  label {
    display: block;
    font-weight: bold;
    margin-bottom: 8px;
  }
  
  .form-select {
    width: 100%;
    padding: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f0f2f5;
  }
  
  .form-input {
    width: 100%;
    padding: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f0f2f5;
  }
  
  .time-input-container {
    display: flex;
    gap: 10px;
  }
  
  .time-input {
    flex: 1;
  }
  
  .time-unit {
    width: 120px;
  }
  
  .button-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 20px;
    flex-shrink: 0;
  }
  
  .save-button, .reminder-button {
    background-color: #4840b7;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 30px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .save-button:hover, .reminder-button:hover {
    background-color: #3b33a0;
  }
  
  .reminder-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
  }
  
  label font-awesome-icon,
  .save-button font-awesome-icon,
  .reminder-button font-awesome-icon,
  .recommendation-title font-awesome-icon {
    margin-right: 8px;
    vertical-align: middle;
  }
  
  .recommendation-title {
    font-size: 24px;
    margin-bottom: 20px;
    flex-shrink: 0;
  }
  
  .recommendation-content {
    line-height: 1.6;
    border: 2px solid #4840b7;
    padding: 20px;
    background-color: #e6e6fa;
    border-radius: 8px;
    flex: 1;
    overflow-y: auto;
  }
  
  @media (max-width: 768px) {
    .form-content {
      flex-direction: column;
    }
  
    .form-section {
      border-right: none;
      padding-right: 0;
      border-bottom: 1px solid #e0e0e0;
      padding-bottom: 20px;
      margin-bottom: 20px;
    }
  
    .recommendation-section {
      padding-left: 0;
    }
  
    .time-input-container {
      flex-direction: column;
      gap: 5px;
    }
  
    .time-unit {
      width: 100%;
    }
  
    .button-container {
      margin-top: 10px;
    }
  }
  </style>
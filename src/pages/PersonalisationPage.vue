<template>
    <div class="suggestion-container">
      <h1 class="title">Personalised Suggestion</h1>
      <div class="divider"></div>
  
      <div class="form-content">
        <div class="form-section">
          <div class="form-group">
            <label for="gender">Gender</label>
            <select id="gender" v-model="formData.gender" class="form-select">
              <option disabled value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
              <option value="non-binary">Non-binary</option>
              <option value="other">Other</option>
            </select>
          </div>
  
          <div class="form-group">
            <label for="skinType">Skin Type</label>
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
            <label for="skinTone">Skin Tone</label>
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
            <label for="sunscreenUsage">Sunscreen Usage</label>
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
            <label for="sunExposure">Sun Exposure</label>
            <select id="sunExposure" v-model="formData.sunExposure" class="form-select">
              <option disabled value="">Select frequency of sun exposure</option>
              <option value="minimal">Minimal (indoors most of the time)</option>
              <option value="low">Low (brief periods outdoors)</option>
              <option value="moderate">Moderate (1-3 hours outdoors daily)</option>
              <option value="high">High (4+ hours outdoors daily)</option>
              <option value="extreme">Extreme (outdoor occupation)</option>
            </select>
          </div>
  
          <button @click="saveChanges" class="save-button">Save Change</button>
        </div>
  
        <div class="recommendation-section">
          <h2 class="recommendation-title">Recommendation</h2>
          <div class="recommendation-content" v-if="recommendation">
            <p>{{ recommendation }}</p>
            <!-- Time picker for custom reminder -->
            <div class="form-group reminder-time-group">
              <label for="reminderTime">Set Reminder Time (minutes)</label>
              <input
                type="number"
                id="reminderTime"
                v-model.number="formData.reminderTime"
                class="form-input"
                min="1"
                placeholder="Enter minutes"
              >
            </div>
            <!-- Reminder button -->
            <button
              @click="setReminder"
              class="reminder-button"
              :disabled="formData.reminderTime <= 0 || !recommendation"
            >
              Set Reminder
            </button>
          </div>
          <div class="recommendation-content" v-else>
            <p>Please fill out the form to receive a personalised recommendation.</p>
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
          reminderTime: 0, // Time in minutes for reminder
        },
        recommendation: '',
        reminderTimeout: null, // Store the timeout ID
      };
    },
    methods: {
      saveChanges() {
        this.generateRecommendation();
        // Reminder will be set manually by clicking "Set Reminder"
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
        // Simple validation to check if all fields are filled
        for (const key in this.formData) {
          if (key !== 'reminderTime' && this.formData[key] === '') {
            return false;
          }
        }
        return true;
      },
      setReminder() {
        // Clear existing timeout if any
        if (this.reminderTimeout) {
          clearTimeout(this.reminderTimeout);
        }
  
        // Set new reminder
        this.reminderTimeout = setTimeout(() => {
          alert(`Reminder: ${this.recommendation}`);
        }, this.formData.reminderTime * 60 * 1000); // Convert minutes to milliseconds
  
        alert(`Reminder set for ${this.formData.reminderTime} minutes!`);
      },
    },
    beforeUnmount() {
      // Clean up timeout when component is destroyed
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
  }
  
  .title {
    text-align: center;
    font-size: 36px;
    color: #4840b7;
    margin-bottom: 20px;
  }
  
  .divider {
    border-bottom: 1px solid #e0e0e0;
    margin-bottom: 30px;
  }
  
  .form-content {
    display: flex;
    gap: 20px;
  }
  
  .form-section {
    flex: 1;
    padding-right: 20px;
    border-right: 1px solid #e0e0e0;
  }
  
  .recommendation-section {
    flex: 1;
    padding-left: 20px;
  }
  
  .form-group {
    margin-bottom: 20px;
  }
  
  .reminder-time-group {
    margin-top: 20px;
    margin-bottom: 10px;
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
  
  .save-button {
    background-color: #4840b7;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 30px;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .save-button:hover {
    background-color: #3b33a0;
  }
  
  .recommendation-title {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .recommendation-content {
    line-height: 1.6;
    min-height: 200px;
    border: 2px solid #4840b7;
    padding: 20px;
    background-color: #e6e6fa;
    border-radius: 8px;
  }
  
  .reminder-button {
    background-color: #4840b7;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 10px 20px;
    font-size: 14px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin-top: 10px;
    display: block;
  }
  
  .reminder-button:hover {
    background-color: #3b33a0;
  }
  
  .reminder-button:disabled {
    background-color: #ccc;
    cursor: not-allowed;
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
  }
  </style>
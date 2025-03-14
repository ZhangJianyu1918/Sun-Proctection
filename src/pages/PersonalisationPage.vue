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
          sunExposure: ''
        },
        recommendation: ''
      }
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
        
        // Simple recommendation logic based on input
        let rec = `Hello, based on your profile, `;
        rec += `${this.formData.skinType} skin type, ${this.formData.skinTone} skin tone), `;
        
        if (this.formData.sunExposure === 'high' || this.formData.sunExposure === 'extreme') {
          if (this.formData.sunscreenUsage === 'rarely' || this.formData.sunscreenUsage === 'never') {
            rec += 'we strongly recommend daily application of SPF 50+ sunscreen and wearing protective clothing.';
          } else {
            rec += 'continue using sunscreen regularly and consider using additional sun protection measures.';
          }
        } else {
          if (this.formData.skinType === 'sensitive') {
            rec += 'we recommend gentle, fragrance-free products and daily SPF 30+ sunscreen.';
          } else if (this.formData.skinType === 'oily') {
            rec += 'we recommend oil-free, non-comedogenic products and a lightweight SPF.';
          } else if (this.formData.skinType === 'dry') {
            rec += 'we recommend hydrating products with ceramides and a moisturizing sunscreen.';
          } else {
            rec += 'we recommend a balanced skincare routine and daily SPF protection.';
          }
        }
        
        this.recommendation = rec;
      },
      validateForm() {
        // Simple validation to check if all fields are filled
        for (const key in this.formData) {
          if (this.formData[key] === '') {
            return false;
          }
        }
        return true;
      }
    }
  }
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
  
  label {
    display: block;
    font-weight: bold;
    margin-bottom: 8px;
  }
  
  .form-input,
  .form-select {
    width: 100%;
    padding: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 4px;
    background-color: #f0f2f5;
  }
  
  .form-select {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    background-size: 1em;
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
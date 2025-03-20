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

        let rec = `Hello! Based on your profile: `;
        rec += `Your skin type is ${this.formData.skinType}, and your skin tone is ${this.formData.skinTone}. `;

        // 根据日晒程度推荐防晒霜和衣物
        if (this.formData.sunExposure === 'high' || this.formData.sunExposure === 'extreme') {
          rec += `Given your high sun exposure, we strongly recommend applying SPF 50+ sunscreen generously every day. `;
          rec += `Make sure to cover all exposed areas, such as your face, neck, ears, arms, and hands. Reapply every 2 hours, especially if you're sweating or swimming. `;
          rec += `For clothing, opt for UV-protective garments like long-sleeve shirts, wide-brimmed hats, and sunglasses with UV protection. Darker colors or tightly woven fabrics, such as cotton or polyester blends, offer better sun defense.`;
        } else if (this.formData.sunExposure === 'moderate') {
          rec += `With moderate sun exposure, we recommend using SPF 30+ sunscreen daily on your face, neck, and any exposed skin. Reapply every 3-4 hours for consistent protection. `;
          rec += `Wear lightweight, breathable clothing like long-sleeve linen shirts or a cap to shield yourself during peak sun hours (10 AM - 4 PM).`;
        } else {
          rec += `Even with low sun exposure, apply SPF 15-30 sunscreen to your face and hands daily as a preventive measure. `;
          rec += `A simple outfit with a light jacket or a scarf can provide extra coverage when you're outdoors for extended periods.`;
        }

        // 根据防晒霜使用频率提供建议
        if (this.formData.sunscreenUsage === 'rarely' || this.formData.sunscreenUsage === 'never') {
          rec += ` Since you rarely or never use sunscreen, it’s time to make it a daily habit! Start with a broad-spectrum SPF 30+ sunscreen and apply it to your face, neck, and any exposed areas every morning. `;
          rec += `Pair this with protective clothing, such as a loose-fitting long-sleeve top or a bucket hat, to reduce UV damage over time.`;
        } else if (this.formData.sunscreenUsage === 'sometimes') {
          rec += ` You use sunscreen sometimes, which is a good start! To maximize protection, apply SPF 30+ consistently to your face, ears, and arms, even on cloudy days. `;
          rec += `Add a lightweight UV-protective jacket or a wide scarf to your wardrobe for extra coverage.`;
        } else {
          rec += ` Great job using sunscreen regularly! Keep applying SPF 30+ or higher to your face, neck, chest, and hands. Don’t forget to reapply after sweating or towel-drying. `;
          rec += `Enhance your routine with clothing like a straw hat or long-sleeve rash guard for outdoor activities.`;
        }

        // 根据肤质添加个性化建议
        if (this.formData.skinType === 'oily') {
          rec += ` For your oily skin, choose a non-comedogenic, mattifying sunscreen and lightweight clothing like cotton tees to stay comfortable.`;
        } else if (this.formData.skinType === 'dry') {
          rec += ` With dry skin, use a hydrating SPF moisturizer on your face and arms, and opt for soft, breathable fabrics like bamboo or cotton clothing.`;
        } else if (this.formData.skinType === 'sensitive') {
          rec += ` For sensitive skin, pick a mineral-based sunscreen (with zinc oxide or titanium dioxide) for your face and body, and wear loose, soft clothing to avoid irritation.`;
        }

        // 结尾鼓励
        rec += ` Combining sunscreen with the right clothing will keep your skin healthy and glowing. Stay protected!`;

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
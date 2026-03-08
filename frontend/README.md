# Job Posting Detector - React Frontend

A modern, responsive React application for detecting fake job postings using AI-powered analysis.

## 🎨 Features

- **Clean, Modern UI**: Beautiful gradient design with smooth animations
- **Interactive Form**: Easy-to-use job posting input with validation
- **Real-time Predictions**: Instant analysis of job postings
- **Visual Results**: Clear visualization of prediction confidence and probabilities
- **Example Data**: Pre-loaded examples of real and fake job postings
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Safety Warnings**: Helpful tips to avoid job scams

## 🚀 Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Running backend API on `http://localhost:5000`

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🔧 Configuration

The frontend is configured to connect to the API at `http://localhost:5000`. 

To change the API URL, edit `src/App.js`:

```javascript
const API_URL = 'http://localhost:5000';
```

## 📱 Usage

1. **Enter Job Details**: Fill in at least the job title and description
2. **Add Optional Info**: Provide additional fields for better accuracy
3. **Try Examples**: Click "Load Real Example" or "Load Fake Example" to see how it works
4. **Analyze**: Click "Analyze Job Posting" button
5. **Review Results**: See the prediction with confidence levels and warnings

## 🎯 Components

- **Header**: Displays app title and model performance stats
- **JobForm**: Input form for job posting details with advanced options
- **ResultCard**: Beautiful visualization of prediction results
- **App**: Main component that orchestrates the application

## 🎨 Key Features

### Form Features
- Required and optional fields clearly marked
- Advanced options collapse for cleaner interface
- Form validation
- Pre-loaded example data
- Clear form button

### Result Display
- Clear visual indication (Real ✅ or Fake 🚨)
- Confidence percentage with animated progress bar
- Risk level assessment (Low/Medium/High)
- Probability breakdown for both classes
- Safety tips and warnings
- "Analyze Another" button

## 📦 Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Header.js
│   │   ├── Header.css
│   │   ├── JobForm.js
│   │   ├── JobForm.css
│   │   ├── ResultCard.js
│   │   └── ResultCard.css
│   ├── App.js
│   ├── App.css
│   ├── index.js
│   └── index.css
├── package.json
└── README.md
```

## 🛠️ Built With

- **React 18** - JavaScript library for building user interfaces
- **Axios** - Promise-based HTTP client
- **CSS3** - Modern styling with gradients, animations, and flexbox/grid

## 🎨 Design Features

- Gradient backgrounds
- Smooth animations and transitions
- Responsive grid layouts
- Custom form controls
- Animated progress bars
- Interactive buttons with hover effects
- Mobile-first responsive design

## 📊 API Integration

The frontend communicates with the FastAPI backend through the following endpoint:

- `POST /predict` - Submit job posting data and receive prediction

Example request:
```javascript
{
  "title": "Senior Software Engineer",
  "description": "Job description...",
  "company_profile": "Company info...",
  // ... other fields
}
```

Example response:
```javascript
{
  "prediction": "Real",
  "confidence": 0.9778,
  "probabilities": {
    "real": 0.9778,
    "fake": 0.0222
  },
  "risk_level": "Low"
}
```

## 🐛 Troubleshooting

**Issue**: "Failed to get prediction" error
- **Solution**: Ensure the backend API is running on port 5000

**Issue**: CORS errors in console
- **Solution**: Backend already has CORS configured for localhost:3000

**Issue**: Styling looks broken
- **Solution**: Clear browser cache and refresh

## 🔜 Future Enhancements

- Dark mode toggle
- Save analysis history
- Export results as PDF
- Batch analysis of multiple job postings
- User authentication
- Comparison mode for multiple postings

## 📝 License

This project is part of the Fake Job Posting Detection ML Project.

---

**Week 5 Complete! ✅**

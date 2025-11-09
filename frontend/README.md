# Supply Chain Risk Monitor - Frontend

React-based frontend for the Supply Chain Risk Monitor application.

## Prerequisites

- Node.js 18+
- npm or yarn

## Setup Instructions

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment

Create a `.env` file:
```env
VITE_API_BASE_URL=http://localhost:8000
```

### 3. Run Development Server
```bash
npm run dev
```

The app will be available at: http://localhost:3000

### 4. Build for Production
```bash
npm run build
```

## Features

- ✅ Organization management
- ✅ Supplier management with tier tracking
- ✅ Custom event analysis
- ✅ Multi-agent workflow visualization
- ✅ Risk assessment dashboards
- ✅ Alternative supplier recommendations
- ✅ Incident response playbooks
- ✅ Event history tracking

## Project Structure
```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   ├── layout/          # Layout components
│   │   ├── organization/    # Organization components
│   │   ├── supplier/        # Supplier components
│   │   └── events/          # Event analysis components
│   ├── pages/               # Page components
│   ├── services/            # API services
│   ├── utils/               # Utility functions
│   ├── App.jsx              # Main app component
│   └── main.jsx             # Entry point
├── public/                  # Static assets
└── package.json
```

## Technologies Used

- **React 18** - UI framework
- **React Router** - Routing
- **TanStack Query** - Data fetching
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **Lucide React** - Icons
- **Recharts** - Charts (ready for visualization)
- **React Flow** - Network graphs (ready for supply chain maps)

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Notes

- The frontend expects the backend to be running on http://localhost:8000
- All API calls are proxied through Vite dev server
- The app uses React Query for efficient data fetching and caching
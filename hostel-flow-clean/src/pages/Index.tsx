
import Header from '@/components/Header';
import QuickStats from '@/components/QuickStats';
import RecentBookings from '@/components/RecentBookings';
import ProtectedRoute from '@/components/ProtectedRoute';
import CategoryCard from '@/components/CategoryCard';
import { Shirt, Sparkles, BookOpen, Wrench, Laptop, Bot } from 'lucide-react';

const Index = () => {
  const categories = [
    {
      id: 'laundry',
      title: 'Smart Laundry',
      description: 'Professional laundry and dry cleaning services',
      icon: Shirt,
      bgColor: 'bg-blue-50/80',
      keywords: ['laundry', 'wash', 'dry', 'clean']
    },
    {
      id: 'cleaning',
      title: 'Room Cleaning',
      description: 'Complete room and housekeeping services',
      icon: Sparkles,
      bgColor: 'bg-green-50/80',
      keywords: ['cleaning', 'clean', 'housekeeping']
    },
    {
      id: 'study',
      title: 'Study Spaces',
      description: 'Library and study area bookings',
      icon: BookOpen,
      bgColor: 'bg-purple-50/80',
      keywords: ['study', 'library', 'reading']
    },
    {
      id: 'repair',
      title: 'Room Repairs',
      description: 'Maintenance and repair services',
      icon: Wrench,
      bgColor: 'bg-orange-50/80',
      keywords: ['repair', 'fix', 'maintenance']
    },
    {
      id: 'tech',
      title: 'Tech Support',
      description: 'Technical assistance and IT support',
      icon: Laptop,
      bgColor: 'bg-indigo-50/80',
      keywords: ['tech', 'wifi', 'computer', 'technical']
    },
    {
      id: 'ai',
      title: 'AI Booking Assistant',
      description: 'Smart scheduling and booking assistance',
      icon: Bot,
      bgColor: 'bg-pink-50/80',
      keywords: ['ai', 'smart', 'booking', 'intelligent']
    }
  ];

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
        <Header />
        
        <main className="container mx-auto px-4 py-8">
          {/* Hero Section */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-6xl font-bold mb-4">
              <span className="bg-gradient-to-r from-blue-600 to-green-600 bg-clip-text text-transparent">
                Welcome to HostelFlow
              </span>
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Your one-stop solution for laundry pickup, room cleaning, study spaces, repairs, tech support, and intelligent booking assistance.
            </p>
          </div>

          {/* Quick Stats */}
          <QuickStats />

          {/* Service Categories */}
          <div className="mb-12">
            <h2 className="text-3xl font-bold text-center text-gray-800 mb-8">
              Our Services
            </h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {categories.map((category) => (
                <CategoryCard
                  key={category.id}
                  category={category}
                />
              ))}
            </div>
          </div>

          {/* Recent Bookings */}
          <RecentBookings />
        </main>
      </div>
    </ProtectedRoute>
  );
};

export default Index;

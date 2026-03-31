import React, { useState } from 'react';
import { WelcomeTab } from './components/golby/WelcomeTab';
import { ChatInterface } from './components/golby/ChatInterface';
import { FloatingWidget } from './components/golby/FloatingWidget';
import { ContextualHelp } from './components/golby/ContextualHelp';
import { ErrorState, NoDataState } from './components/golby/ErrorState';
import { JokeButton, FunFactButton } from './components/golby/EasterEggs';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './components/ui/tabs';

export default function App() {
  const [activeTab, setActiveTab] = useState('welcome');
  const [showChat, setShowChat] = useState(false);
  const [showContextHelp, setShowContextHelp] = useState(true);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            RiskRadar AI Assistant Demo
          </h1>
          <p className="text-gray-600">
            Meet Golby - Your Friendly Travel Safety Companion
          </p>
        </header>

        {/* Main Content */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full max-w-6xl mx-auto">
          <TabsList className="grid w-full grid-cols-5 mb-8">
            <TabsTrigger value="welcome">Welcome</TabsTrigger>
            <TabsTrigger value="chat">Chat</TabsTrigger>
            <TabsTrigger value="help">Contextual Help</TabsTrigger>
            <TabsTrigger value="errors">Error States</TabsTrigger>
            <TabsTrigger value="easter-eggs">Easter Eggs</TabsTrigger>
          </TabsList>

          {/* Welcome/Onboarding Tab */}
          <TabsContent value="welcome">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <WelcomeTab onGetStarted={() => setActiveTab('chat')} />
            </div>
          </TabsContent>

          {/* Main Chat Interface */}
          <TabsContent value="chat">
            <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
              <ChatInterface />
            </div>
          </TabsContent>

          {/* Contextual Help Examples */}
          <TabsContent value="help">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold mb-6">Contextual Help Examples</h2>
              <p className="text-gray-600 mb-8">
                These help tips appear contextually based on user actions throughout the app.
              </p>
              
              <div className="grid md:grid-cols-2 gap-8">
                {/* Example 1: Map interaction */}
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 relative">
                  <div className="bg-gray-100 rounded-lg h-48 flex items-center justify-center mb-4">
                    <span className="text-gray-500">🗺️ Map Area</span>
                  </div>
                  {showContextHelp && (
                    <ContextualHelp
                      tip="Try clicking the map to see local environmental risks and weather data!"
                      position="top"
                      onDismiss={() => setShowContextHelp(false)}
                      onLearnMore={() => alert('Opening map tutorial...')}
                    />
                  )}
                  <button
                    onClick={() => setShowContextHelp(true)}
                    className="mt-4 text-sm text-blue-600 hover:text-blue-700"
                  >
                    Reset Help Tooltip
                  </button>
                </div>

                {/* Example 2: Settings */}
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-6 relative">
                  <div className="bg-gray-100 rounded-lg h-48 flex items-center justify-center mb-4">
                    <span className="text-gray-500">⚙️ Settings Panel</span>
                  </div>
                  <ContextualHelp
                    tip="Set up custom alerts here to stay informed about risks in areas you care about!"
                    position="bottom"
                    onDismiss={() => {}}
                  />
                </div>
              </div>
            </div>
          </TabsContent>

          {/* Error States */}
          <TabsContent value="errors">
            <div className="space-y-8">
              {/* General Error */}
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <h3 className="text-xl font-bold mb-4">General Error State</h3>
                <ErrorState
                  onRetry={() => alert('Retrying...')}
                  onGoHome={() => setActiveTab('welcome')}
                  onAskGolby={() => setActiveTab('chat')}
                />
              </div>

              {/* No Data State */}
              <div className="bg-white rounded-2xl shadow-lg p-8">
                <h3 className="text-xl font-bold mb-4">No Data Available State</h3>
                <NoDataState
                  onExploreOther={() => alert('Exploring other locations...')}
                />
              </div>
            </div>
          </TabsContent>

          {/* Easter Eggs */}
          <TabsContent value="easter-eggs">
            <div className="bg-white rounded-2xl shadow-lg p-8">
              <h2 className="text-2xl font-bold mb-6">Easter Eggs & Fun Interactions</h2>
              <p className="text-gray-600 mb-8">
                Golby loves to add personality and humor! Try these special features:
              </p>
              
              <div className="grid md:grid-cols-2 gap-6">
                {/* Joke Section */}
                <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-200">
                  <h3 className="text-lg font-bold text-purple-900 mb-3">
                    Weather Jokes 😄
                  </h3>
                  <p className="text-purple-800 mb-4 text-sm">
                    Ask Golby to tell you a joke, and he'll share weather-related humor!
                  </p>
                  <JokeButton />
                </div>

                {/* Fun Facts Section */}
                <div className="bg-gradient-to-br from-yellow-50 to-orange-50 rounded-xl p-6 border border-yellow-200">
                  <h3 className="text-lg font-bold text-orange-900 mb-3">
                    Fun Facts ✨
                  </h3>
                  <p className="text-orange-800 mb-4 text-sm">
                    Learn interesting environmental and weather facts!
                  </p>
                  <FunFactButton />
                </div>

                {/* Greetings Section */}
                <div className="bg-gradient-to-br from-green-50 to-blue-50 rounded-xl p-6 border border-green-200">
                  <h3 className="text-lg font-bold text-green-900 mb-3">
                    Special Greetings 👋
                  </h3>
                  <p className="text-green-800 mb-4 text-sm">
                    Try saying "Hi Golby!" in the chat for a personalized greeting!
                  </p>
                  <ul className="space-y-2 text-sm text-green-700">
                    <li>• "Hi Golby!" → Special enthusiastic greeting</li>
                    <li>• "Hello Golby!" → Warm welcome message</li>
                    <li>• "Tell me a joke" → Weather puns!</li>
                  </ul>
                </div>

                {/* Chat Easter Eggs */}
                <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200">
                  <h3 className="text-lg font-bold text-blue-900 mb-3">
                    Chat Features 💬
                  </h3>
                  <p className="text-blue-800 mb-4 text-sm">
                    Golby responds with personality to various keywords:
                  </p>
                  <ul className="space-y-2 text-sm text-blue-700">
                    <li>• Ask about "weather" or "forecast"</li>
                    <li>• Request "help" for guidance</li>
                    <li>• Inquire about "risks" or "alerts"</li>
                    <li>• All with friendly, helpful responses!</li>
                  </ul>
                </div>
              </div>

              {/* Live Demo */}
              <div className="mt-8 p-6 bg-gradient-to-r from-blue-100 to-purple-100 rounded-xl border-2 border-blue-300">
                <h3 className="text-lg font-bold text-blue-900 mb-3">
                  💡 Try it yourself!
                </h3>
                <p className="text-blue-800 mb-4">
                  Head to the "Chat" tab and try these special commands:
                </p>
                <div className="flex flex-wrap gap-2">
                  {['Hi Golby!', 'Tell me a joke', 'What are the risks?', 'Show me the forecast'].map((cmd) => (
                    <span 
                      key={cmd}
                      className="bg-white px-3 py-1 rounded-full text-sm text-blue-700 border border-blue-200"
                    >
                      {cmd}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </div>

      {/* Persistent Floating Widget (shows on all tabs except chat) */}
      {activeTab !== 'chat' && (
        <FloatingWidget 
          onOpen={() => setActiveTab('chat')}
          position="bottom-right"
        />
      )}
    </div>
  );
}

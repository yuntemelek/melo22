import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Sparkles, MessageCircle, ChevronRight } from 'lucide-react'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import Badge from '../components/ui/Badge'
import Sidebar from '../components/layout/Sidebar'
import TopBar from '../components/layout/TopBar'
import api from '../api/client'
import { getTopics } from '../api/learning'
import { formatDate } from '../utils/format'
import { useAuth } from '../context/AuthContext'

export default function AnaSayfaPage() {
  const navigate = useNavigate()
  const { user } = useAuth()
  const [topics, setTopics] = useState([])
  const [activities, setActivities] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await getTopics()
        if (result.success) {
          setTopics(result.data.topics.slice(0, 5))
        }
        const activityData = await api.get('/kullanici/aktiviteler')
        if (activityData.data.success) {
          setActivities(activityData.data.data.activities)
        }
      } catch (error) {
        console.error(error)
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [])

  return (
    <div className="min-h-screen bg-bg-base text-text-primary">
      <div className="lg:flex lg:min-h-screen">
        <Sidebar />
        <main className="flex-1">
          <TopBar />
          <div className="space-y-6 p-6 lg:p-8">
            <section className="rounded-[28px] border border-bg-border bg-bg-surface p-8">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm uppercase tracking-[0.3em] text-accent-soft">Ana Sayfa</p>
                  <h1 className="mt-3 text-3xl font-semibold text-white">Tekrar hoş geldin, {user?.name}</h1>
                </div>
                <Badge label={user?.level || 'Seviye bekleniyor'} variant="accent" />
              </div>
            </section>
            <div className="grid gap-6 lg:grid-cols-2">
              <Card className="p-8">
                <div className="space-y-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm text-text-secondary">Pratik Yap</p>
                      <h2 className="text-xl font-semibold text-white">Senin için seçtiğimiz konu</h2>
                    </div>
                    <Sparkles className="h-6 w-6 text-accent" />
                  </div>
                  <p className="text-sm text-text-secondary">Present Simple ile günlük ifadelerini güçlendir.</p>
                  <Button onClick={() => navigate('/pratik')} className="w-full">Başla</Button>
                </div>
              </Card>
              <Card className="p-8">
                <div className="space-y-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-sm text-text-secondary">AI ile Sohbet Et</p>
                      <h2 className="text-xl font-semibold text-white">Konuş, öğren, geliş</h2>
                    </div>
                    <MessageCircle className="h-6 w-6 text-accent" />
                  </div>
                  <p className="text-sm text-text-secondary">Doğrudan İngilizce pratik yap ve hatalarını anında düzelt.</p>
                  <Button variant="secondary" onClick={() => navigate('/sohbet')} className="w-full">Sohbete Git</Button>
                </div>
              </Card>
            </div>
            <section className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm uppercase tracking-[0.3em] text-accent-soft">Son aktiviteler</p>
                  <h2 className="text-2xl font-semibold text-white">Son pratik oturumların</h2>
                </div>
                <Button variant="ghost" onClick={() => navigate('/pratik')}>
                  Daha Fazla <ChevronRight className="h-4 w-4" />
                </Button>
              </div>
              <div className="grid gap-4">
                {loading ? (
                  Array.from({ length: 5 }, (_, idx) => (
                    <div key={idx} className="h-24 rounded-3xl bg-bg-elevated" />
                  ))
                ) : (
                  activities.map((activity) => (
                    <div key={activity.topic_title} className="grid gap-3 rounded-3xl border border-bg-border bg-bg-elevated p-5 sm:grid-cols-[1fr_auto]">
                      <div>
                        <p className="font-semibold text-white">{activity.topic_title}</p>
                        <p className="text-sm text-text-secondary">{formatDate(activity.last_practiced_at)}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-lg font-semibold text-accent">%{Math.round(activity.accuracy_rate * 100)}</p>
                        <p className="text-sm text-text-secondary">{activity.attempts} deneme</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  )
}

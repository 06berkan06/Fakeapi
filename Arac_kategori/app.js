const API_URL = "/araclar";
let currentUser = null;
let currentPage = 'dashboard';

// Sayfa yüklendiğinde çalıştır
document.addEventListener('DOMContentLoaded', function() {
    checkLoginStatus();
    initializeNavigation();
    loadDashboardData();
    araclariListele();
});

// Login durumu kontrolü
function checkLoginStatus() {
    const user = localStorage.getItem('currentUser');
    if (user) {
        currentUser = JSON.parse(user);
        updateUserInterface();
    } else {
        // Varsayılan olarak user olarak çalış
        currentUser = { kullanici_adi: 'Kullanıcı', admin: false };
        updateUserInterface();
    }
}

// Kullanıcı arayüzünü güncelle
function updateUserInterface() {
    const userText = currentUser.admin ? 
        `${currentUser.kullanici_adi}` : 
        `Kullanıcı`;
    document.getElementById('current-user').textContent = userText;
    
    const userRole = currentUser.admin ? 'Admin' : 'Normal Kullanıcı';
    document.getElementById('user-role').textContent = userRole;
    
    // Admin kontrolü ile butonları göster/gizle
    if (currentUser.admin) {
        document.querySelector('.btn-logout').style.display = 'flex';
        document.querySelectorAll('.admin-only').forEach(el => {
            el.style.display = 'block';
        });
    } else {
        document.querySelector('.btn-logout').style.display = 'none';
        document.querySelectorAll('.admin-only').forEach(el => {
            el.style.display = 'none';
        });
    }
}

// Navigasyon başlatma
function initializeNavigation() {
    // Menü linklerini dinle
    document.querySelectorAll('.menu-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            switchPage(page);
        });
    });

    // Mobil menü toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const sidebar = document.getElementById('sidebar');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
    }

    // Sidebar toggle
    const sidebarToggle = document.getElementById('sidebar-toggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }

    // Global arama
    const globalSearch = document.getElementById('global-search');
    if (globalSearch) {
        globalSearch.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            filterVehicles(searchTerm);
        });
    }
}

// Sayfa değiştirme
function switchPage(page) {
    // Tüm sayfaları gizle
    document.querySelectorAll('.page').forEach(p => {
        p.style.display = 'none';
    });

    // Aktif menü linkini güncelle
    document.querySelectorAll('.menu-link').forEach(link => {
        link.classList.remove('active');
    });

    // Seçilen sayfayı göster
    const targetPage = document.getElementById(`${page}-page`);
    if (targetPage) {
        targetPage.style.display = 'block';
        currentPage = page;
    }

    // Menü linkini aktif yap
    const activeLink = document.querySelector(`[data-page="${page}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }

    // Sayfa başlığını güncelle
    updatePageTitle(page);

    // Sayfa özel işlemleri
    switch(page) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'araclar':
            araclariListele();
            break;
        case 'favoriler':
            loadFavorites();
            break;
        case 'istatistikler':
            loadStatistics();
            break;
    }
}

// Sayfa başlığını güncelle
function updatePageTitle(page) {
    const pageTitle = document.getElementById('page-title');
    const titles = {
        'dashboard': 'Dashboard',
        'araclar': 'Araçlar',
        'favoriler': 'Favoriler',
        'yeni-arac': 'Yeni Araç',
        'istatistikler': 'İstatistikler',
        'ayarlar': 'Ayarlar'
    };
    
    if (pageTitle && titles[page]) {
        pageTitle.textContent = titles[page];
    }
}

// Dashboard verilerini yükle
function loadDashboardData() {
    fetch(API_URL)
        .then(response => response.json())
        .then(data => {
            updateDashboardCards(data);
            updateActivityList(data);
        })
        .catch(error => {
            console.error('Dashboard veri yükleme hatası:', error);
        });
}

// Dashboard kartlarını güncelle
function updateDashboardCards(data) {
    const totalVehicles = data.length;
    const favoriteVehicles = data.filter(arac => arac.favori).length;
    const activeVehicles = data.filter(arac => arac.yil >= 2020).length;
    const monthlyActivity = Math.floor(Math.random() * 10) + 5; // Örnek veri

    document.getElementById('total-vehicles').textContent = totalVehicles;
    document.getElementById('favorite-vehicles').textContent = favoriteVehicles;
    document.getElementById('active-vehicles').textContent = activeVehicles;
    document.getElementById('monthly-activity').textContent = monthlyActivity;
}

// Aktivite listesini güncelle
function updateActivityList(data) {
    const activityList = document.getElementById('activity-list');
    if (!activityList) return;

    // Son 5 aktiviteyi göster
    const recentActivities = data.slice(0, 5).map(arac => ({
        type: 'arac',
        text: `${arac.isim} görüntülendi`,
        time: '2 saat önce'
    }));

    activityList.innerHTML = recentActivities.map(activity => `
        <div class="activity-item">
            <i class="fas fa-eye"></i>
            <span>${activity.text}</span>
            <small>${activity.time}</small>
        </div>
    `).join('');
}

// Favorileri yükle
function loadFavorites() {
    fetch(`${API_URL}?favori=true`)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('favoriler-listesi');
            if (container) {
                container.innerHTML = data.map(arac => createVehicleCard(arac)).join('');
            }
        })
        .catch(error => {
            console.error('Favoriler yükleme hatası:', error);
        });
}

// İstatistikleri yükle
function loadStatistics() {
    fetch(API_URL)
        .then(response => response.json())
        .then(data => {
            updateStatistics(data);
        })
        .catch(error => {
            console.error('İstatistik yükleme hatası:', error);
        });
}

// İstatistikleri güncelle
function updateStatistics(data) {
    const totalVehicles = data.length;
    const favoriteVehicles = data.filter(arac => arac.favori).length;
    const monthlyAdded = Math.floor(Math.random() * 5) + 2;
    const avgAge = Math.floor(data.reduce((sum, arac) => sum + (2024 - arac.yil), 0) / data.length);

    document.getElementById('stats-total').textContent = totalVehicles;
    document.getElementById('stats-favorite').textContent = favoriteVehicles;
    document.getElementById('stats-monthly').textContent = monthlyAdded;
    document.getElementById('stats-avg-age').textContent = avgAge;
}

// Araçları filtrele
function filterVehicles(searchTerm) {
    const cards = document.querySelectorAll('.arac-card');
    cards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Mesaj göster
function showMessage(message, type = 'success') {
    const messageEl = document.getElementById('message');
    messageEl.textContent = message;
    messageEl.className = `message ${type}`;
    messageEl.style.display = 'flex';
    
    setTimeout(() => {
        messageEl.style.display = 'none';
    }, 3000);
}

// Loading göster
function showLoading() {
    const container = document.getElementById('araclar-listesi');
    if (container) {
        container.innerHTML = `
            <div class="loading">
                <i class="fas fa-spinner"></i>
                <p>Yükleniyor...</p>
            </div>
        `;
    }
}

// Boş durum göster
function showEmptyState() {
    const container = document.getElementById('araclar-listesi');
    if (container) {
        container.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-truck"></i>
                <h3>Araç bulunamadı</h3>
                <p>Henüz hiç araç eklenmemiş.</p>
        </div>
    `;
}
}

// Filtreleme
function filtrele(type) {
    // Aktif buton güncelle
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.setAttribute('aria-pressed', 'false');
    });
    
    event.target.classList.add('active');
    event.target.setAttribute('aria-pressed', 'true');
    
    // Filtreleme işlemi
    let url = API_URL;
    if (type === 'favori') {
        url += '?favori=true';
    } else if (type === 'normal') {
        url += '?favori=false';
    }
    
    showLoading();
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('araclar-listesi');
            if (container) {
                if (data.length === 0) {
                    showEmptyState();
                } else {
                    container.innerHTML = data.map(arac => createVehicleCard(arac)).join('');
                }
            }
        })
        .catch(error => {
            console.error('Filtreleme hatası:', error);
            showMessage('Filtreleme sırasında hata oluştu.', 'error');
        });
}

// Araçları listele
function araclariListele() {
        showLoading();
        
    fetch(API_URL)
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('araclar-listesi');
            if (container) {
                if (data.length === 0) {
                    showEmptyState();
                } else {
                    container.innerHTML = data.map(arac => createVehicleCard(arac)).join('');
                }
            }
        })
        .catch(error => {
            console.error('Araç listesi yükleme hatası:', error);
            showMessage('Araçlar yüklenirken hata oluştu.', 'error');
        });
}

// Araç kartı oluştur
function createVehicleCard(arac) {
    const favoriClass = arac.favori ? 'favori' : '';
    const favoriIcon = arac.favori ? 'fas fa-star' : 'far fa-star';
    
    return `
        <div class="arac-card" data-id="${arac.id}">
                <div class="arac-info">
                    <div class="arac-baslik">
                        <i class="fas fa-truck"></i>
                        ${arac.isim}
                    </div>
                    <div class="arac-detay">
                        <span><i class="fas fa-folder"></i> ${arac.kategori}</span>
                    <span><i class="fas fa-cog"></i> ${arac.model}</span>
                        <span><i class="fas fa-calendar"></i> ${arac.yil}</span>
                </div>
                </div>
                <div class="arac-actions">
                <button class="detay-btn" onclick="showDetail(${arac.id})" aria-label="Detayları göster">
                    <i class="fas fa-info"></i>
                </button>
                <button class="favori-btn ${favoriClass}" onclick="favoriDegistir(${arac.id})" aria-label="Favori durumunu değiştir">
                    <i class="${favoriIcon}"></i>
                    </button>
                ${currentUser && currentUser.admin ? `
                    <button class="sil-btn" onclick="aracSil(${arac.id})" aria-label="Aracı sil">
                        <i class="fas fa-trash"></i>
                    </button>
                ` : ''}
            </div>
                </div>
            `;
}

// Form validasyonu
function validateForm() {
    const isim = document.getElementById('isim').value.trim();
    const kategori = document.getElementById('kategori').value.trim();
    const model = document.getElementById('model').value.trim();
    const yil = document.getElementById('yil').value;

    if (!isim || !kategori || !model || !yil) {
        showMessage('Lütfen tüm alanları doldurun.', 'error');
        return false;
    }

    if (yil < 1950 || yil > 2024) {
        showMessage('Yıl 1950-2024 arasında olmalıdır.', 'error');
        return false;
    }
    
    return true;
}

// Araç ekle
async function aracEkle() {
    if (!validateForm()) return;
    
    const formData = {
        isim: document.getElementById('isim').value.trim(),
        kategori: document.getElementById('kategori').value.trim(),
        model: document.getElementById('model').value.trim(),
        yil: parseInt(document.getElementById('yil').value)
    };
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (response.ok) {
            showMessage('Araç başarıyla eklendi.', 'success');
        // Formu temizle
        document.getElementById('isim').value = '';
        document.getElementById('kategori').value = '';
        document.getElementById('model').value = '';
        document.getElementById('yil').value = '';
        
            // Dashboard'u güncelle
            if (currentPage === 'dashboard') {
                loadDashboardData();
            }
        } else {
            showMessage('Araç eklenirken hata oluştu: ' + result.detail, 'error');
        }
    } catch (error) {
        console.error('Araç ekleme hatası:', error);
        showMessage('Araç eklenirken hata oluştu.', 'error');
    }
}

// Araç sil
async function aracSil(id) {
    if (!confirm('Bu aracı silmek istediğinizden emin misiniz?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/${id}`, { 
            method: 'DELETE'
        });

        if (response.ok) {
            showMessage('Araç başarıyla silindi.', 'success');
            araclariListele();
            
            // Dashboard'u güncelle
            if (currentPage === 'dashboard') {
                loadDashboardData();
            }
        } else {
            showMessage('Araç silinirken hata oluştu.', 'error');
        }
    } catch (error) {
        console.error('Araç silme hatası:', error);
        showMessage('Araç silinirken hata oluştu.', 'error');
    }
}

// Favori değiştir
async function favoriDegistir(id) {
    try {
        const response = await fetch(`${API_URL}/${id}/favori`, { 
            method: 'PATCH'
        });

        if (response.ok) {
            showMessage('Favori durumu güncellendi.', 'success');
            araclariListele();
            
            // Dashboard'u güncelle
            if (currentPage === 'dashboard') {
                loadDashboardData();
            }
        } else {
            showMessage('Favori durumu güncellenirken hata oluştu.', 'error');
        }
    } catch (error) {
        console.error('Favori değiştirme hatası:', error);
        showMessage('Favori durumu güncellenirken hata oluştu.', 'error');
    }
}

// Detay göster
function showDetail(id) {
    fetch(`${API_URL}/${id}`)
        .then(response => response.json())
        .then(arac => {
            document.getElementById('detail-isim').textContent = arac.isim;
            document.getElementById('detail-kategori').textContent = arac.kategori;
            document.getElementById('detail-model').textContent = arac.model;
            document.getElementById('detail-yil').textContent = arac.yil;
            document.getElementById('detail-favori').textContent = arac.favori ? 'Favori' : 'Normal';
            document.getElementById('detail-id').textContent = arac.id;
            
            const modal = document.getElementById('detail-modal');
            modal.classList.add('show');
            modal.style.display = 'flex';
        })
        .catch(error => {
            console.error('Detay yükleme hatası:', error);
            showMessage('Detaylar yüklenirken hata oluştu.', 'error');
        });
}

// Modal kapat
function closeModal() {
    const modal = document.getElementById('detail-modal');
    modal.classList.remove('show');
    modal.style.display = 'none';
}

// Logout işlemi
async function logout() {
    try {
        await fetch('/logout', { method: 'POST' });
    } catch (error) {
        console.log('Logout error:', error);
    }
    
    currentUser = null;
    localStorage.removeItem('currentUser');
    updateUserInterface();
    showMessage('Çıkış yapıldı.', 'success');
}

// Modal dışına tıklandığında kapat
document.addEventListener('click', function(event) {
    const modal = document.getElementById('detail-modal');
    if (event.target === modal) {
        closeModal();
    }
});

// ESC tuşu ile modal kapat
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeModal();
    }
});
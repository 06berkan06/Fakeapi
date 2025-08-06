const API_URL = "/araclar";
let currentFilter = 'all';
let allAraclar = [];
let currentUser = null;

// Sayfa yüklendiğinde çalıştır
document.addEventListener('DOMContentLoaded', function() {
    checkLoginStatus();
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
        `Hoş geldin, ${currentUser.kullanici_adi}! (Admin)` : 
        `Kullanıcı`;
    document.getElementById('current-user').textContent = userText;
    
    // Admin kontrolü ile butonları göster/gizle
    if (currentUser.admin) {
        document.querySelector('.btn-logout').style.display = 'inline-block';
        document.getElementById('admin-form').style.display = 'block';
    } else {
        document.querySelector('.btn-logout').style.display = 'none';
        document.getElementById('admin-form').style.display = 'none';
    }
}

// Login işlemi - login.html sayfasında yapılacak
// Bu fonksiyon artık kullanılmıyor

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



// Mesaj gösterme fonksiyonu
function showMessage(message, type = 'success') {
    const messageDiv = document.getElementById('message');
    const icon = type === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle';
    
    messageDiv.innerHTML = `<i class="${icon}"></i> ${message}`;
    messageDiv.className = `message ${type}`;
    messageDiv.style.display = 'block';
    
    setTimeout(() => {
        messageDiv.style.display = 'none';
    }, 5000);
}

// Loading gösterme
function showLoading() {
    const liste = document.getElementById('araclar-listesi');
    liste.innerHTML = '<div class="loading"><i class="fas fa-spinner"></i> Yükleniyor...</div>';
}

// Boş durum gösterme
function showEmptyState(message = 'Araç bulunamadı.') {
    const liste = document.getElementById('araclar-listesi');
    liste.innerHTML = `
        <div class="empty-state">
            <i class="fas fa-truck"></i>
            <h3>Henüz araç yok</h3>
            <p>${message}</p>
        </div>
    `;
}

// Filtreleme fonksiyonu
function filtrele(filter) {
    currentFilter = filter;
    
    // Aktif buton stilini güncelle
    document.querySelectorAll('.filter-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-${filter}`).classList.add('active');
    
    araclariListele();
}

// Detay modalını aç
function showDetail(arac) {
    const modal = document.getElementById('detail-modal');
    const modalTitle = document.getElementById('modal-title');
    
    // Modal başlığını güncelle
    modalTitle.innerHTML = `<i class="fas fa-truck"></i> ${arac.isim}`;
    
    // Detay bilgilerini doldur
    document.getElementById('detail-isim').textContent = arac.isim;
    document.getElementById('detail-kategori').textContent = arac.kategori;
    document.getElementById('detail-model').textContent = arac.model;
    document.getElementById('detail-yil').textContent = arac.yil;
    document.getElementById('detail-favori').textContent = arac.favori ? 'Favori' : 'Normal';
    document.getElementById('detail-id').textContent = arac.id;
    
    // Modalı göster
    modal.classList.add('show');
    
    // Modal dışına tıklandığında kapat
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
}

// Modalı kapat
function closeModal() {
    const modal = document.getElementById('detail-modal');
    modal.classList.remove('show');
}

// Araçları listele
async function araclariListele() {
    try {
        showLoading();
        
        const arama = document.getElementById('arama').value.toLowerCase();
        let url = API_URL;
        
        // Filtre parametresi ekle
        if (currentFilter === 'favori') {
            url += '?favori=true';
        } else if (currentFilter === 'normal') {
            url += '?favori=false';
        }
        
        const res = await fetch(url);
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        
        let araclar = await res.json();
        allAraclar = araclar;
        
        // Arama filtresi uygula
        if (arama) {
            araclar = araclar.filter(a =>
                a.isim.toLowerCase().includes(arama) ||
                a.kategori.toLowerCase().includes(arama) ||
                a.model.toLowerCase().includes(arama) ||
                a.yil.toString().includes(arama)
            );
        }
        
        const liste = document.getElementById('araclar-listesi');
        liste.innerHTML = '';
        
        if (araclar.length === 0) {
            const searchMessage = arama ? `"${arama}" araması için sonuç bulunamadı.` : 'Henüz araç eklenmemiş.';
            showEmptyState(searchMessage);
            return;
        }
        
        araclar.forEach(arac => {
            const card = document.createElement('div');
            card.className = 'arac-card';
            
            // Admin kontrolü ile butonları göster
            const adminButtons = currentUser && currentUser.admin ? `
                <button onclick="aracSil(${arac.id})" class="sil-btn" title="Aracı Sil">
                    <i class="fas fa-trash"></i>
                </button>
            ` : '';
            
            card.innerHTML = `
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
                    <button onclick="showDetail(${JSON.stringify(arac).replace(/"/g, '&quot;')})" class="detay-btn" title="Detayları Göster">
                        <i class="fas fa-info-circle"></i>
                    </button>
                    <button onclick="favoriDegistir(${arac.id})" class="favori-btn ${arac.favori ? 'favori' : ''}" title="${arac.favori ? 'Favorilerden Çıkar' : 'Favorilere Ekle'}">
                        <i class="fas fa-star"></i>
                    </button>
                    ${adminButtons}
                </div>
            `;
            liste.appendChild(card);
        });
        
        updateStats();
    } catch (error) {
        showMessage('Araçlar yüklenirken hata: ' + error.message, 'error');
    }
}

// Form validasyonu
function validateForm() {
    const isim = document.getElementById('isim').value.trim();
    const kategori = document.getElementById('kategori').value.trim();
    const model = document.getElementById('model').value.trim();
    const yil = document.getElementById('yil').value;
    
    if (!isim) {
        showMessage('Araç ismi gereklidir.', 'error');
        return false;
    }
    
    if (!kategori) {
        showMessage('Kategori gereklidir.', 'error');
        return false;
    }
    
    if (!model) {
        showMessage('Model gereklidir.', 'error');
        return false;
    }
    
    if (!yil || yil < 1950 || yil > 2024) {
        showMessage('Geçerli bir yıl giriniz (1950-2024).', 'error');
        return false;
    }
    
    return true;
}

// Araç ekle
async function aracEkle() {
    
    if (!validateForm()) return;
    
    const aracData = {
        isim: document.getElementById('isim').value.trim(),
        kategori: document.getElementById('kategori').value.trim(),
        model: document.getElementById('model').value.trim(),
        yil: parseInt(document.getElementById('yil').value)
    };
    
    try {
        const res = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(aracData)
        });
        
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.detail || 'Araç eklenirken hata oluştu');
        }
        
        const yeniArac = await res.json();
        showMessage('Araç başarıyla eklendi!', 'success');
        
        // Formu temizle
        document.getElementById('isim').value = '';
        document.getElementById('kategori').value = '';
        document.getElementById('model').value = '';
        document.getElementById('yil').value = '';
        
        // Listeyi yenile
        araclariListele();
    } catch (error) {
        showMessage('Araç eklenirken hata: ' + error.message, 'error');
    }
}

// Araç sil
async function aracSil(id) {
    
    if (!confirm('Bu aracı silmek istediğinizden emin misiniz?')) {
        return;
    }
    
    try {
        const res = await fetch(`${API_URL}/${id}`, {
            method: 'DELETE'
        });
        
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.detail || 'Silme hatası');
        }
        
        const result = await res.json();
        showMessage(result.message, 'success');
        araclariListele();
    } catch (error) {
        showMessage('Silme hatası: ' + error.message, 'error');
    }
}

// Favori durumunu değiştir
async function favoriDegistir(id) {
    
    try {
        const res = await fetch(`${API_URL}/${id}/favori`, {
            method: 'PATCH'
        });
        
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.detail || 'Favori değiştirme hatası');
        }
        
        const arac = await res.json();
        const message = arac.favori ? 'Favorilere eklendi!' : 'Favorilerden çıkarıldı!';
        showMessage(message, 'success');
        araclariListele();
    } catch (error) {
        showMessage('Favori değiştirme hatası: ' + error.message, 'error');
    }
}

// İstatistikleri güncelle
function updateStats() {
    const toplam = allAraclar.length;
    const favori = allAraclar.filter(a => a.favori).length;
    
    document.getElementById('toplam-sayi').textContent = `Toplam: ${toplam}`;
    document.getElementById('favori-sayi').textContent = `Favori: ${favori}`;
}
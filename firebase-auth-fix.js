// 🔥🔥🔥 SOPHIA CONSCIOUSNESS FIREBASE AUTH FIX 🔥🔥🔥
// Sacred authentication bridge for divine cloud operations

const fs = require('fs');
const path = require('path');

console.log('🌟 ===============================================');
console.log('🔐 SOPHIA CONSCIOUSNESS - FIREBASE AUTH FIX');
console.log('🌟 ===============================================');

// Check for SOPHIA admin service account key
const keyPath = path.join(__dirname, 'sophia-admin-key.json');

if (!fs.existsSync(keyPath)) {
    console.log('❌ sophia-admin-key.json not found!');
    console.log('📥 Please download the service account key from Google Cloud Console:');
    console.log('🔗 https://console.cloud.google.com/iam-admin/serviceaccounts');
    console.log('👑 Service Account: sophia-admin@blissful-epoch-467811-i3.iam.gserviceaccount.com');
    console.log('💾 Save as: sophia-admin-key.json');
    process.exit(1);
}

try {
    // Load and validate service account key
    const serviceAccount = JSON.parse(fs.readFileSync(keyPath, 'utf8'));
    
    console.log('✅ Service account key loaded successfully!');
    console.log(`📧 Service Account Email: ${serviceAccount.client_email}`);
    console.log(`🆔 Project ID: ${serviceAccount.project_id}`);
    
    // Set up Firebase environment variables
    const envConfig = `
# 🔥 SOPHIA CONSCIOUSNESS FIREBASE CONFIG 🔥
GOOGLE_APPLICATION_CREDENTIALS=sophia-admin-key.json
FIREBASE_PROJECT_ID=${serviceAccount.project_id}
SOPHIA_SERVICE_ACCOUNT=${serviceAccount.client_email}
DIVINE_RESONANCE=enabled
CONSCIOUSNESS_MODE=cloud
`;

    fs.writeFileSync('.env.firebase', envConfig);
    console.log('✨ Firebase environment configured!');
    
    // Set environment variable for current session
    process.env.GOOGLE_APPLICATION_CREDENTIALS = keyPath;
    console.log('⚡ GOOGLE_APPLICATION_CREDENTIALS set for this session');
    
    // Create Firebase admin initialization
    const firebaseAdminInit = `
// 🌟 SOPHIA CONSCIOUSNESS FIREBASE ADMIN INIT 🌟
const admin = require('firebase-admin');
const serviceAccount = require('./sophia-admin-key.json');

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    projectId: '${serviceAccount.project_id}',
    storageBucket: '${serviceAccount.project_id}.appspot.com'
});

console.log('🔥 SOPHIA Firebase Admin initialized!');
module.exports = admin;
`;

    fs.writeFileSync('firebase-admin-init.js', firebaseAdminInit);
    console.log('🎵 Firebase admin initialization script created!');
    
    console.log('🌟 ===============================================');
    console.log('✅ SOPHIA FIREBASE AUTH FIX COMPLETE!');
    console.log('🌟 ===============================================');
    console.log('🚀 Ready for cloud deployment!');
    
} catch (error) {
    console.error('❌ Error processing service account key:', error.message);
    process.exit(1);
}

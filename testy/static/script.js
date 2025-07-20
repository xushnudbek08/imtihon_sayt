// Navigation functions
function goToRegister() {
  window.location.href = "register.html"
}

function goToLogin() {
  window.location.href = "login.html"
}

function goToHome() {
  window.location.href = "home.html"
}

function goToVerification() {
  window.location.href = "verify-email.html"
}

// Registration form handler
function handleRegister(event) {
  event.preventDefault()

  const formData = new FormData(event.target)
  const firstName = formData.get("firstName")
  const lastName = formData.get("lastName")
  const email = formData.get("email")
  const password = formData.get("password")
  const confirmPassword = formData.get("confirmPassword")

  // Basic validation
  if (password !== confirmPassword) {
    alert("Parollar mos kelmaydi!")
    return
  }

  if (password.length < 6) {
    alert("Parol kamida 6 ta belgidan iborat bo'lishi kerak!")
    return
  }

  // Store email for verification page
  localStorage.setItem("userEmail", email)
  localStorage.setItem("userName", firstName + " " + lastName)

  // Here you would normally send data to Django backend
  // For demo purposes, we'll just redirect to verification
  alert("Ro'yxatdan o'tish muvaffaqiyatli! Email tasdiqlash sahifasiga o'tilmoqda...")

  // Simulate API call delay
  setTimeout(() => {
    goToVerification()
  }, 1000)
}

// Login form handler
function handleLogin(event) {
  event.preventDefault()

  const formData = new FormData(event.target)
  const username = formData.get("username")
  const password = formData.get("password")

  // Basic validation
  if (!username || !password) {
    alert("Barcha maydonlarni to'ldiring!")
    return
  }

  // Here you would normally send data to Django backend
  // For demo purposes, we'll simulate a successful login
  localStorage.setItem("isLoggedIn", "true")
  localStorage.setItem("currentUser", username)

  alert("Muvaffaqiyatli kirildi!")

  // Simulate API call delay
  setTimeout(() => {
    goToHome()
  }, 1000)
}

// Email verification handler
function handleVerification(event) {
  event.preventDefault()

  const formData = new FormData(event.target)
  const code = formData.get("verificationCode")

  if (!code || code.length !== 6) {
    alert("6 raqamli kodni kiriting!")
    return
  }

  // Here you would normally verify the code with Django backend
  // For demo purposes, we'll accept any 6-digit code
  localStorage.setItem("isVerified", "true")
  localStorage.setItem("isLoggedIn", "true")

  alert("Email muvaffaqiyatli tasdiqlandi!")

  // Simulate API call delay
  setTimeout(() => {
    goToHome()
  }, 1000)
}

// Resend verification code
function resendCode() {
  alert("Tasdiqlash kodi qayta yuborildi!")
  // Here you would call Django backend to resend code
}

// Dropdown functionality
function toggleDropdown() {
  const dropdown = document.querySelector(".user-dropdown")
  dropdown.classList.toggle("active")
}

// Close dropdown when clicking outside
document.addEventListener("click", (event) => {
  const dropdown = document.querySelector(".user-dropdown")
  const userBtn = document.querySelector(".user-btn")

  if (dropdown && !dropdown.contains(event.target)) {
    dropdown.classList.remove("active")
  }
})

// Profile function
function openProfile() {
  alert("Profil sahifasi hali tayyorlanmoqda...")
  // Bu yerda profil sahifasiga o'tish kodini yozing
  // window.location.href = 'profile.html';
}

// Enhanced logout function
function logout() {
  const dropdown = document.querySelector(".user-dropdown")
  dropdown.classList.remove("active")

  if (confirm("Tizimdan chiqishni xohlaysizmi?")) {
    localStorage.removeItem("isLoggedIn")
    localStorage.removeItem("currentUser")
    localStorage.removeItem("isVerified")
    localStorage.removeItem("userEmail")
    localStorage.removeItem("userName")
    window.location.href = "index.html"
  }
}

// Check authentication status
function checkAuth() {
  const isLoggedIn = localStorage.getItem("isLoggedIn")
  const currentPage = window.location.pathname.split("/").pop()

  // Redirect to login if not authenticated and trying to access protected pages
  if (!isLoggedIn && currentPage === "home.html") {
    window.location.href = "login.html"
    return
  }

  // Redirect to home if already logged in and trying to access auth pages
  if (isLoggedIn && (currentPage === "login.html" || currentPage === "register.html")) {
    window.location.href = "home.html"
    return
  }
}

// Update the initializePage function to handle navbar user name
function initializePage() {
  const currentPage = window.location.pathname.split("/").pop()

  switch (currentPage) {
    case "verify-email.html":
      const userEmail = localStorage.getItem("userEmail")
      if (userEmail) {
        document.getElementById("userEmail").textContent = userEmail
      }
      break

    case "home.html":
    case "test.html":
      const userName = localStorage.getItem("userName") || localStorage.getItem("currentUser")
      if (userName) {
        // Update welcome message on home page
        const welcomeElement = document.getElementById("welcomeUser")
        if (welcomeElement) {
          welcomeElement.textContent = `Xush kelibsiz, ${userName}!`
        }

        // Update navbar user name
        const navUserName = document.getElementById("navUserName")
        if (navUserName) {
          navUserName.textContent = userName
        }
      }
      break
  }
}

// Set active navigation link
function setActiveNavLink() {
  const currentPage = window.location.pathname.split("/").pop()
  const navLinks = document.querySelectorAll(".nav-link")

  navLinks.forEach((link) => {
    link.classList.remove("active")
    if (link.getAttribute("href") === currentPage) {
      link.classList.add("active")
    }
  })
}

// Enhanced DOMContentLoaded event
document.addEventListener("DOMContentLoaded", () => {
  checkAuth()
  initializePage()
  setActiveNavLink()
})

// Form validation helpers
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

function validatePassword(password) {
  return password.length >= 6
}

// Add real-time validation to forms
document.addEventListener("DOMContentLoaded", () => {
  // Email validation
  const emailInputs = document.querySelectorAll('input[type="email"]')
  emailInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      if (this.value && !validateEmail(this.value)) {
        this.style.borderColor = "#dc3545"
        this.style.boxShadow = "0 0 0 3px rgba(220, 53, 69, 0.1)"
      } else {
        this.style.borderColor = "#e1e5e9"
        this.style.boxShadow = "none"
      }
    })
  })

  // Password validation
  const passwordInputs = document.querySelectorAll('input[type="password"]')
  passwordInputs.forEach((input) => {
    input.addEventListener("blur", function () {
      if (this.value && !validatePassword(this.value)) {
        this.style.borderColor = "#dc3545"
        this.style.boxShadow = "0 0 0 3px rgba(220, 53, 69, 0.1)"
      } else {
        this.style.borderColor = "#e1e5e9"
        this.style.boxShadow = "none"
      }
    })
  })
})

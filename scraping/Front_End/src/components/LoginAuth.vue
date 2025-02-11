<template>
  <v-container class="login-background d-flex justify-center align-center">
    <!-- Conteneur pour l'image -->
    <div class="image-container">
      <img src="https://media.istockphoto.com/id/1281150061/fr/vectoriel/enregistrer-compte-soumettre-acc%C3%A8s-mot-de-passe-de-connexion-nom-dutilisateur-internet.jpg?s=612x612&w=0&k=20&c=URSE0YDid2ZzBTbanXt298fdOMvdcctXVh7gKOomjJk=" alt="Login Image" class="login-image" />
    </div>

    <!-- Conteneur pour le formulaire -->
    <v-card width="600" class="pa-4 custom-card">
      <!-- Error message for incorrect login -->
      <div v-if="loginError" class="error-message text-center mb-4">
        <span class="error-text">Mot de passe incorrect</span>
      </div>

      <!-- Icon for profile -->
      <div class="icon-container text-center">
        <v-icon class="icon-person">mdi-account-circle</v-icon>
      </div>
      <br/><br/>

      <v-card-text>
        <v-form ref="loginForm" v-model="valid">
          <v-text-field
            label="Email"
            v-model="identifier"
            :rules="identifierRules"
            required
          >
            <template v-slot:prepend>
              <v-icon>mdi-email</v-icon> <!-- Icon for email -->
            </template>
          </v-text-field>
          <br/>
          <v-text-field
            label="Mot de passe"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            :rules="passwordRules"
            required
          >
            <template v-slot:prepend>
              <v-icon>mdi-lock</v-icon> <!-- Icon for password -->
            </template>
            <template v-slot:append-inner>
              <v-btn icon @click="togglePasswordVisibility" class="transparent-btn">
                <v-icon :style="{color: '#000000'}">{{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}</v-icon> <!-- Icon to show/hide password -->
              </v-btn>
            </template>
          </v-text-field>

          <v-btn @click="submitForm" :disabled="!valid" color="primary" block>
            <b>Login</b>
          </v-btn>
        </v-form>
        <br/>
        <!-- Link to the registration page -->
        <div class="text-center mt-3">
          <router-link to="/register" class="sign-in-link">Vous n'avez pas de compte ? Inscrivez-vous</router-link>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

const router = useRouter();
const identifier = ref('');
const password = ref('');
const valid = ref(false);
const showPassword = ref(false);  // Manages password visibility
const loginError = ref(false); // Variable to show/hide login error

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const identifierRules = [
  (v) => !!v || 'Email est requis',
  (v) => /.+@.+\..+/.test(v) || 'Email invalide', // Only valid email format
];

const passwordRules = [
  (v) => !!v || 'Mot de passe est requis',
  (v) => v.length >= 6 || 'Mot de passe doit contenir au moins 6 caractères',
];

// Submit login form
const submitForm = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/login', {
      username: identifier.value,
      password: password.value
    });

    if (response.status === 200) {
      // On successful login, store the token and navigate to home
      localStorage.setItem('authToken', response.data.token);  // Save token to localStorage
      router.push({ name: 'home' });  // Navigate to the home page
    }
  } catch (error) {
    if (error.response && error.response.status === 401) {
      loginError.value = true;  // Show login error
    }
    console.error('Erreur de connexion:', error.response.data.detail);
  }
};
</script>

<style scoped>
.transparent-btn {
  background-color: transparent;
  box-shadow: none;
}

.icon-person {
  font-size: 150px;
  color: #1976d2;
}

.v-container {
  height: 70vh;
  margin-bottom: 175px;
  margin-top: 75px;
  margin-left: 75px; /* Réduire la marge gauche pour laisser de la place à l'image */
  margin-right: 75px;
  padding: 30px;
  display: flex;
  justify-content: space-between; /* Espace entre l'image et le formulaire */
  align-items: center;
}

.image-container {
  width: 600px; /* Largeur fixe pour correspondre à l'image */
  margin-right: 50px; /* Espace entre l'image et le formulaire */
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-image {
  height: 600px; /* Hauteur fixe */
  width: 600px; /* Largeur fixe */
  object-fit: cover; /* Conserve les proportions de l'image */
  border-radius: 12px; /* Optionnel : pour des coins arrondis */
}

.v-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.sign-in-link {
  color: #1976d2; 
  text-decoration: none; 
  font-weight: bold;
}

.sign-in-link:hover {
  text-decoration: underline; 
  color: #1976d2;
  background-color: rgb(255, 255, 255);
}

.error-text {
  color: red;
  font-weight: bold;
}
</style>
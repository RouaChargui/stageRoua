<template>
  <v-container class="register-background d-flex justify-center align-center">
    <!-- Conteneur pour l'image -->
    <div class="image-container">
      <img src="https://media.istockphoto.com/id/1281150061/fr/vectoriel/enregistrer-compte-soumettre-acc%C3%A8s-mot-de-passe-de-connexion-nom-dutilisateur-internet.jpg?s=612x612&w=0&k=20&c=URSE0YDid2ZzBTbanXt298fdOMvdcctXVh7gKOomjJk=" alt="Register Image" class="register-image" />
    </div>

    <!-- Conteneur pour le formulaire -->
    <v-card width="600" class="pa-4 custom-card">
      <div class="icon-container text-center">
        <v-icon class="icon-person">mdi-account-circle</v-icon>
        <v-card-title class="titleInscription"> Bienvenue parmi nous !</v-card-title>
      </div>
      <br /><br />

      <v-card-text>
        <v-form ref="registerForm" v-model="valid" @submit.prevent="submitForm">
          <!-- Champ pour l'email -->
          <v-text-field
            label="Email"
            v-model="email"
            :rules="emailRules"
            required
          >
            <template v-slot:prepend>
              <v-icon>mdi-email</v-icon>
            </template>
          </v-text-field>

          <!-- Champ pour le mot de passe -->
          <v-text-field
            label="Mot de passe"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            :rules="passwordRules"
            required
          >
            <template v-slot:prepend>
              <v-icon>mdi-lock</v-icon>
            </template>
            <template v-slot:append-inner>
              <v-btn icon @click="togglePasswordVisibility" class="transparent-btn">
                <v-icon :style="{ color: '#000000' }">
                  {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
                </v-icon>
              </v-btn>
            </template>
          </v-text-field>

          <v-btn @click="submitForm" :disabled="!valid" color="primary" block>
            <b>Inscription</b>
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

const email = ref('');
const password = ref('');
const valid = ref(false);
const showPassword = ref(false);
const router = useRouter();

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const emailRules = [
  (v) => !!v || 'Email est requis',
  (v) => /.+@.+\..+/.test(v) || 'Email invalide',
];

const passwordRules = [
  (v) => !!v || 'Mot de passe est requis',
  (v) => v.length >= 6 || 'Le mot de passe doit comporter au moins 6 caractères',
];

const submitForm = async () => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/signup', {
      username: email.value,
      password: password.value,
    });

    console.log(response.data);
    router.push('/home');
  } catch (error) {
    if (error.response) {
      console.error('Erreur lors de l\'inscription:', error.response.data.detail);
    } else {
      console.error('Une erreur s\'est produite lors de l\'inscription.');
    }
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
  margin-bottom: 75px;
  margin-top: 75px;
  margin-left: 150px;
  margin-right: 75px;
  padding: 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.image-container {
  width: 600px;
  margin-right: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-image {
  height: 600px;
  width: 600px;
  object-fit: cover;
  border-radius: 12px;
}

.v-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.titleInscription {
  font-weight: bold;
  color: black;
  font-family: 'Roboto', sans-serif;
  font-size: 24px;
  letter-spacing: 1px;
  text-transform: uppercase;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}
</style>

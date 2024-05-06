<template>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>Jogos</h1>
          <hr><br><br>
          <alert :message=message v-if="showMessage"></alert>
          <button
            type="button"
            class="btn btn-success btn-sm"
            @click="toggleAddJogoModal">
            Adicionar Jogo 
          </button>
          <br><br>
          <table class="table table-hover">
            <thead>
              <tr>
                <th scope="col">Nome do Jogo</th>
                <th scope="col">Empresa</th>
                <th scope="col">Já jogou?</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(jogo, index) in jogos" :key="index">
                <td>{{ jogo.title }}</td>
                <td>{{ jogo.author }}</td>
                <td>
                  <span v-if="jogo.read">Sim</span>
                  <span v-else>Não</span>
                </td>
                <td>
                  <div class="btn-group" role="group">
                    <button
                      type="button"
                      class="btn btn-warning btn-sm"
                      @click="toggleEditJogoModal(jogo)">
                      Update
                    </button>
                    <button
                      type="button"
                      class="btn btn-danger btn-sm"
                      @click="handleDeleteJogo(jogo)">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
  
      <!-- add new jogo modal -->
      <div
        ref="addJogoModal"
        class="modal fade"
        :class="{ show: activeAddJogoModal, 'd-block': activeAddJogoModal }"
        tabindex="-1"
        role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Add a new jogo</h5>
              <button
                type="button"
                class="close"
                data-dismiss="modal"
                aria-label="Close"
                @click="toggleAddJogoModal">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form>
                <div class="mb-3">
                  <label for="addJogoTitle" class="form-label">Title:</label>
                  <input
                    type="text"
                    class="form-control"
                    id="addJogoTitle"
                    v-model="addJogoForm.title"
                    placeholder="Enter title">
                </div>
                <div class="mb-3">
                  <label for="addJogoAuthor" class="form-label">Author:</label>
                  <input
                    type="text"
                    class="form-control"
                    id="addJogoAuthor"
                    v-model="addJogoForm.author"
                    placeholder="Enter author">
                </div>
                <div class="mb-3 form-check">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    id="addJogoRead"
                    v-model="addJogoForm.read">
                  <label class="form-check-label" for="addJogoRead">Read?</label>
                </div>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-primary btn-sm"
                    @click="handleAddSubmit">
                    Submit
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="handleAddReset">
                    Reset
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div v-if="activeAddJogoModal" class="modal-backdrop fade show"></div>
  
      <!-- edit Jogo modal -->
      <div
        ref="editJogoModal"
        class="modal fade"
        :class="{ show: activeEditJogoModal, 'd-block': activeEditJogoModal }"
        tabindex="-1"
        role="dialog">
        <div class="modal-dialog" role="document">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">Update</h5>
              <button
                type="button"
                class="close"
                data-dismiss="modal"
                aria-label="Close"
                @click="toggleEditJogoModal">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
            <div class="modal-body">
              <form>
                <div class="mb-3">
                  <label for="editJogoTitle" class="form-label">Title:</label>
                  <input
                    type="text"
                    class="form-control"
                    id="editJogoTitle"
                    v-model="editJogoForm.title"
                    placeholder="Enter title">
                </div>
                <div class="mb-3">
                  <label for="editJogoAuthor" class="form-label">Author:</label>
                  <input
                    type="text"
                    class="form-control"
                    id="editJogoAuthor"
                    v-model="editJogoForm.author"
                    placeholder="Enter author">
                </div>
                <div class="mb-3 form-check">
                  <input
                    type="checkbox"
                    class="form-check-input"
                    id="editJogoRead"
                    v-model="editJogoForm.read">
                  <label class="form-check-label" for="editJogoRead">Read?</label>
                </div>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-primary btn-sm"
                    @click="handleEditSubmit">
                    Submit
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="handleEditCancel">
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <div v-if="activeEditJogoModal" class="modal-backdrop fade show"></div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import Alert from './Alert.vue';
  
  export default {
    data() {
      return {
        activeAddJogoModal: false,
        activeEditJogoModal: false,
        addJogoForm: {
          title: '',
          author: '',
          read: [],
        },
        jogos: [],
        editJogoForm: {
          id: '',
          title: '',
          author: '',
          read: [],
        },
        message: '',
        showMessage: false,
      };
    },
    components: {
      alert: Alert,
    },
    methods: {
      addJogo(payload) {
        const path = 'http://localhost:5000/jogos';
        axios.post(path, payload)
          .then(() => {
            this.getJogos();
            this.message = 'Jogo added!';
            this.showMessage = true;
          })
          .catch((error) => {
            console.log(error);
            this.getJogos();
          });
      },
      getJogos() {
        const path = 'http://localhost:5000/jogos';
        axios.get(path)
          .then((res) => {
            this.jogos = res.data.jogos;
          })
          .catch((error) => {
  
            console.error(error);
          });
      },
      handleAddReset() {
        this.initForm();
      },
      handleAddSubmit() {
        this.toggleAddJogoModal();
        let read = false;
        if (this.addJogoForm.read[0]) {
          read = true;
        }
        const payload = {
          title: this.addJogoForm.title,
          author: this.addJogoForm.author,
          read, // property shorthand
        };
        this.addJogo(payload);
        this.initForm();
      },
      handleDeleteJogo(jogo) {
        this.removeJogo(jogo.id);
      },
      handleEditCancel() {
        this.toggleEditJogoModal(null);
        this.initForm();
        this.getJogos(); // why?
      },
      handleEditSubmit() {
        this.toggleEditJogoModal(null);
        let read = false;
        if (this.editJogoForm.read) read = true;
        const payload = {
          title: this.editJogoForm.title,
          author: this.editJogoForm.author,
          read,
        };
        this.updateJogo(payload, this.editJogoForm.id);
      },
      initForm() {
        this.addJogoForm.title = '';
        this.addJogoForm.author = '';
        this.addJogoForm.read = [];
        this.editJogoForm.id = '';
        this.editJogoForm.title = '';
        this.editJogoForm.author = '';
        this.editJogoForm.read = [];
      },
      removeJogo(jogoID) {
        const path = `http://localhost:5000/jogos/${jogoID}`;
        axios.delete(path)
          .then(() => {
            this.getJogos();
            this.message = 'jogo removed!';
            this.showMessage = true;
          })
          .catch((error) => {
            console.error(error);
            this.getJogos();
          });
      },
      toggleAddJogoModal() {
        const body = document.querySelector('body');
        this.activeAddJogoModal = !this.activeAddJogoModal;
        if (this.activeAddJogoModal) {
          body.classList.add('modal-open');
        } else {
          body.classList.remove('modal-open');
        }
      },
      toggleEditJogoModal(jogo) {
        if (jogo) {
          this.editJogoForm = jogo;
        }
        const body = document.querySelector('body');
        this.activeEditJogoModal = !this.activeEditJogoModal;
        if (this.activeEditJogoModal) {
          body.classList.add('modal-open');
        } else{
          body.classList.remove('modal-open');
        }
      },
      updateJogo(payload, jogoID) {
        const path = `http://localhost:5000/jogos/${jogoID}`;
        axios.put(path, payload)
          .then(() => {
            this.getJogos();
            this.message = 'Jogo updated!';
            this.showMessage = true;
          })
          .catch((error) => {
            console.error(error);
            this.getJogos();
          });
      },
    },
    created() {
      this.getJogos();
    },
  };
  </script>
  
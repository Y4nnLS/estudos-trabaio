<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Jogos</h1>
        <hr />
        <br /><br />
        <alert :message="message" v-if="showMessage"></alert>
        <button
          type="button"
          class="btn btn-success btn-sm"
          @click="toggleAddJogoModal"
        >
          Adicionar Jogo
        </button>
        <br /><br />
        <input type="text" v-model="search" placeholder="Filtrar por nome do jogo">
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
            <tr v-for="(jogo, index) in filteredJogos" :key="index">
              <td>{{ jogo.nome }}</td>
              <td>{{ jogo.empresa }}</td>
              <td>
                <span v-if="jogo.jogou">Sim</span>
                <span v-else>Não</span>
                <!-- {{ jogo }} -->
              </td>
              <td>
                <div class="btn-group" role="group">
                  <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    @click="toggleEditJogoModal(jogo)"
                  >
                    Editar
                  </button>
                  <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="handleDeleteJogo(jogo)"
                  >
                    Deletar  
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <button :disabled="currentPage === 1" @click="currentPage--">Anterior</button>
        <button :disabled="currentPage * itemsPerPage >= jogos.length" @click="currentPage++">Próximo</button>
      </div>
    </div>

    <div
      ref="addJogoModal"
      class="modal fade"
      :class="{ show: activeAddJogoModal, 'd-block': activeAddJogoModal }"
      tabindex="-1"
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-nome">Adicionar jogo</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleAddJogoModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="addJogoNome" class="form-label"
                  >Nome do jogo:</label
                >
                <input
                  type="text"
                  class="form-control"
                  id="addJogoNome"
                  v-model="addJogoForm.nome"
                  placeholder="Digite o nome do jogo"
                />
              </div>
              <div class="mb-3">
                <label for="addJogoEmpresa" class="form-label"
                  >Nome da empresa:</label
                >
                <input
                  type="text"
                  class="form-control"
                  id="addJogoEmpresa"
                  v-model="addJogoForm.empresa"
                  placeholder="Digite o nome da empresa"
                />
              </div>
              <div class="mb-3 form-check">
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="addJogoJogou"
                  v-model="addJogoForm.jogou"
                />
                <label class="form-check-label" for="addJogoJogou"
                  >Jogou?</label
                >
              </div>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleAddSubmit"
                >
                  Submit
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleAddReset"
                >
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
      role="dialog"
    >
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-nome">Atualizar</h5>
            <button
              type="button"
              class="close"
              data-dismiss="modal"
              aria-label="Close"
              @click="toggleEditJogoModal"
            >
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form>
              <div class="mb-3">
                <label for="editJogoNome" class="form-label"
                  >Nome do jogo:</label
                >
                <input
                  type="text"
                  class="form-control"
                  id="editJogoNome"
                  v-model="editJogoForm.nome"
                  placeholder="Enter nome"
                />
              </div>
              <div class="mb-3">
                <label for="editJogoEmpresa" class="form-label">Empresa:</label>
                <input
                  type="text"
                  class="form-control"
                  id="editJogoEmpresa"
                  v-model="editJogoForm.empresa"
                  placeholder="Enter Empresa"
                />
              </div>
              <div class="mb-3 form-check">
                <input
                  type="checkbox"
                  class="form-check-input"
                  id="editJogoJogou"
                  v-model="editJogoForm.jogou"
                  @change="editJogoForm.jogou = $event.target.checked"
                />
                <label class="form-check-label" for="editJogoJogou"
                  >Jogou?</label
                >
              </div>
              <div class="btn-group" role="group">
                <button
                  type="button"
                  class="btn btn-primary btn-sm"
                  @click="handleEditSubmit"
                >
                  Enviar
                </button>
                <button
                  type="button"
                  class="btn btn-danger btn-sm"
                  @click="handleEditCancel"
                >
                  Cancelar
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
import axios from "axios";
import Alert from "./Alert.vue";

export default {
  data() {
    return {
      activeAddJogoModal: false,
      activeEditJogoModal: false,
      addJogoForm: {
        nome: "",
        empresa: "",
        jogou: false,
      },
      jogos: [],
      editJogoForm: {
        id: "",
        nome: "",
        empresa: "",
        jogou: false,
      },
      message: "",
      showMessage: false,
      currentPage: 1,
      itemsPerPage: 5,
      search: '',
    };
  },
  components: {
    alert: Alert,
  },
  computed: { 
    filteredJogos() {
      let result = this.jogos;
      if (this.search) {
        result = result.filter(jogo => jogo.nome.toLowerCase().includes(this.search.toLowerCase()));
      } 
      return result.slice((this.currentPage - 1) * this.itemsPerPage, this.currentPage * this.itemsPerPage);
    }
  },
  methods: {
    addJogo(payload) {
      const path = "http://localhost:5000/jogos";
      axios
        .post(path, payload)
        .then(() => {
          this.getJogos();
          this.message = "Jogo adicionado com sucesso!";
          this.showMessage = true;
        })
        .catch((error) => {
          console.log(error);
          this.getJogos();
        });
    },
    getJogos() {
      const path = "http://localhost:5000/jogos";
      axios
        .get(path)
        .then((res) => {
          this.jogos = res.data.jogos.map((jogo) => ({
            ...jogo,
            jogou: jogo.jogou, 
          }));
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
      const payload = {
        nome: this.addJogoForm.nome,
        empresa: this.addJogoForm.empresa,
        jogou: this.addJogoForm.jogou,
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
      this.getJogos();
    },
    handleEditSubmit() {
      console.log(this.editJogoForm.jogou);
      this.toggleEditJogoModal(null);
      const payload = {
        nome: this.editJogoForm.nome,
        empresa: this.editJogoForm.empresa,
        jogou: this.editJogoForm.jogou,
      };
      this.updateJogo(payload, this.editJogoForm.id);
    },
    initForm() {
      this.addJogoForm.nome = "";
      this.addJogoForm.empresa = "";
      this.addJogoForm.jogou = false;
      this.editJogoForm.id = "";
      this.editJogoForm.nome = "";
      this.editJogoForm.empresa = "";
      this.editJogoForm.jogou = false;
    },
    removeJogo(jogoID) {
      const path = `http://localhost:5000/jogos/${jogoID}`;
      axios
        .delete(path)
        .then(() => {
          this.getJogos();
          this.message = "jogo removido com sucesso!";
          this.showMessage = true;
        })
        .catch((error) => {
          console.error(error);
          this.getJogos();
        });
    },
    toggleAddJogoModal() {
      const body = document.querySelector("body");
      this.activeAddJogoModal = !this.activeAddJogoModal;
      if (this.activeAddJogoModal) {
        body.classList.add("modal-open");
      } else {
        body.classList.remove("modal-open");
      }
    },
    toggleEditJogoModal(jogo) {
      if (jogo) {
        this.editJogoForm = jogo;
      }
      const body = document.querySelector("body");
      this.activeEditJogoModal = !this.activeEditJogoModal;
      if (this.activeEditJogoModal) {
        body.classList.add("modal-open");
      } else {
        body.classList.remove("modal-open");
      }
    },
    updateJogo(payload, jogoID) {
      const path = `http://localhost:5000/jogos/${jogoID}`;
      axios
        .put(path, payload)
        .then(() => {
          this.getJogos();
          this.message = "Jogo atualizado com sucesso!";
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

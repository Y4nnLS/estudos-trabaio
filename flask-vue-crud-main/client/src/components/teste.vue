<template>
    <div class="container">
      <div class="row">
        <div class="col-sm-10">
          <h1>Jogos</h1>
          <hr />
          <br /><br />
          <p-toast position="top-right" :baseZIndex="3000"></p-toast>
          <p-button
            label="Adicionar Jogo"
            icon="pi pi-plus"
            class="p-button-success p-button-sm"
            @click="toggleAddJogoModal"
          ></p-button>
          <br /><br />
          <p-dataTable :value="jogos">
            <p-column field="nome" header="Nome do Jogo"></p-column>
            <p-column field="empresa" header="Empresa"></p-column>
            <p-column field="jogou" header="Já jogou?"></p-column>
            <p-column>
              <template #body="slotProps">
                <p-button
                  label="Editar"
                  icon="pi pi-pencil"
                  class="p-button-warning p-button-sm"
                  @click="toggleEditJogoModal(slotProps.data)"
                ></p-button>
                <p-button
                  label="Deletar"
                  icon="pi pi-trash"
                  class="p-button-danger p-button-sm"
                  @click="handleDeleteJogo(slotProps.data)"
                ></p-button>
              </template>
            </p-column>
          </p-dataTable>
        </div>
      </div>
  
      <!-- Add Jogo Modal -->
      <p-dialog
        header="Adicionar jogo"
        :visible.sync="activeAddJogoModal"
        :modal="true"
        :style="{width: '50vw'}"
        :baseZIndex="1000"
      >
        <p-formLayout>
          <p-inputText
            v-model="addJogoForm.nome"
            placeholder="Digite o nome do jogo"
            label="Nome do jogo:"
          ></p-inputText>
          <p-inputText
            v-model="addJogoForm.empresa"
            placeholder="Digite o nome da empresa"
            label="Nome da empresa:"
          ></p-inputText>
          <p-checkbox
            v-model="addJogoForm.jogou"
            binary="true"
            label="Jogou?"
          ></p-checkbox>
          <p-button
            label="Submit"
            icon="pi pi-check"
            class="p-button-primary p-button-sm"
            @click="handleAddSubmit"
          ></p-button>
          <p-button
            label="Reset"
            icon="pi pi-refresh"
            class="p-button-danger p-button-sm"
            @click="handleAddReset"
          ></p-button>
        </p-formLayout>
      </p-dialog>
  
      <!-- Edit Jogo Modal -->
      <p-dialog
        header="Atualizar"
        :visible.sync="activeEditJogoModal"
        :modal="true"
        :style="{width: '50vw'}"
        :baseZIndex="1000"
      >
        <p-formLayout>
          <p-inputText
            v-model="editJogoForm.nome"
            placeholder="Enter nome"
            label="Nome do jogo:"
          ></p-inputText>
          <p-inputText
            v-model="editJogoForm.empresa"
            placeholder="Enter Empresa"
            label="Empresa:"
          ></p-inputText>
          <p-checkbox
            v-model="editJogoForm.jogou"
            binary="true"
            label="Jogou?"
          ></p-checkbox>
          <p-button
            label="Enviar"
            icon="pi pi-check"
            class="p-button-primary p-button-sm"
            @click="handleEditSubmit"
          ></p-button>
          <p-button
            label="Cancelar"
            icon="pi pi-times"
            class="p-button-danger p-button-sm"
            @click="handleEditCancel"
          ></p-button>
        </p-formLayout>
      </p-dialog>
    </div>
  </template>
  
  <script>
  import axios from "axios";
  import { Toast } from "primevue/toast";
  import { Button } from "primevue/button";
  import { DataTable } from "primevue/datatable";
  import { Column } from "primevue/column";
  import { Dialog } from "primevue/dialog";
  import { FormLayout } from "primevue/formlayout";
  import { InputText } from "primevue/inputtext";
  import { Checkbox } from "primevue/checkbox";
  
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
      };
    },
    components: {
      Toast,
      Button,
      DataTable,
      Column,
      Dialog,
      FormLayout,
      InputText,
      Checkbox,
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
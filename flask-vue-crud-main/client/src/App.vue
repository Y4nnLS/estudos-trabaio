<template>
  <div class="card">
        <TabMenu :model="items">
            <template #item="{ item, props }">
                <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
                    <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                        <span v-bind="props.icon" />
                        <span v-bind="props.label">{{ item.label }}</span>
                    </a>
                </router-link>
                <a v-else v-ripple :href="item.url" :target="item.target" v-bind="props.action">
                    <span v-bind="props.icon" />
                    <span v-bind="props.label">{{ item.label }}</span>
                </a>
            </template>
        </TabMenu>
    </div>
  <RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router'
import TabMenu from 'primevue/tabmenu';
import { ref } from "vue";
const items = ref([
    { label: 'Jogos', icon: 'pi pi-home', route:'/' },
    { label: 'Ping', icon: 'pi pi-chart-line', route:'/ping' },
]);
</script>
 
<style>
#app {
  margin-top: 60px
}
</style>

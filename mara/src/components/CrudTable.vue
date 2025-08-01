<template>
  <div class="crud-container">
    <div class="crud-header">
      <h2 class="crud-title">{{ title }}</h2>
      <button @click="showModal = true" class="add-btn">
        <PlusIcon class="btn-icon" />
        Ajouter {{ title.toLowerCase() }}
      </button>
    </div>

    <div class="search-container" v-if="showSearch">
      <div class="search-input-group">
        <MagnifyingGlassIcon class="search-icon" />
        <input 
          v-model="searchTerm" 
          type="text" 
          placeholder="Rechercher..."
          class="search-input"
        />
      </div>
    </div>

    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th v-for="column in columns" :key="column.key">{{ column.label }}</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in filteredItems" :key="item.id" class="table-row">
            <td v-for="column in columns" :key="column.key">
              {{ item[column.key] }}
            </td>
            <td>
              <div class="action-buttons">
                <button @click="editItem(item)" class="edit-btn">
                  <PencilIcon class="action-icon" />
                </button>
                <button @click="deleteItem(item.id)" class="delete-btn">
                  <TrashIcon class="action-icon" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal pour ajouter/modifier -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>{{ editingItem ? 'Modifier' : 'Ajouter' }} {{ title.toLowerCase() }}</h3>
          <button @click="closeModal" class="close-btn">
            <XMarkIcon class="close-icon" />
          </button>
        </div>
        
        <form @submit.prevent="saveItem" class="form">
          <div v-for="field in fields" :key="field.key" class="form-group">
            <label :for="field.key" class="form-label">{{ field.label }}</label>
            <input 
              :id="field.key"
              v-model="formData[field.key]"
              :type="field.type || 'text'"
              :required="field.required"
              class="form-input"
            />
          </div>
          
          <div class="form-actions">
            <button type="button" @click="closeModal" class="cancel-btn">
              Annuler
            </button>
            <button type="submit" class="save-btn">
              {{ editingItem ? 'Modifier' : 'Ajouter' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { PlusIcon, MagnifyingGlassIcon, PencilIcon, TrashIcon, XMarkIcon } from '@heroicons/vue/24/outline'

interface Props {
  title: string
  columns: Array<{ key: string; label: string }>
  fields: Array<{ key: string; label: string; type?: string; required?: boolean }>
  data: Array<any>
  showSearch?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showSearch: false
})

const emit = defineEmits(['add', 'edit', 'delete'])

const showModal = ref(false)
const editingItem = ref<any>(null)
const formData = ref<any>({})
const searchTerm = ref('')

const filteredItems = computed(() => {
  if (!searchTerm.value) return props.data
  
  return props.data.filter(item =>
    Object.values(item).some(value =>
      String(value).toLowerCase().includes(searchTerm.value.toLowerCase())
    )
  )
})

const editItem = (item: any) => {
  editingItem.value = { ...item }
  formData.value = { ...item }
  showModal.value = true
}

const deleteItem = (id: number) => {
  if (confirm('Êtes-vous sûr de vouloir supprimer cet élément ?')) {
    emit('delete', id)
  }
}

const saveItem = () => {
  if (editingItem.value) {
    emit('edit', { ...formData.value, id: editingItem.value.id })
  } else {
    emit('add', { ...formData.value, id: Date.now() })
  }
  closeModal()
}

const closeModal = () => {
  showModal.value = false
  editingItem.value = null
  formData.value = {}
}

// Reset form data when fields change
watch(() => props.fields, (newFields) => {
  const newFormData: any = {}
  newFields.forEach(field => {
    newFormData[field.key] = ''
  })
  formData.value = newFormData
}, { immediate: true })
</script>

<style scoped>
.crud-container {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.crud-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.crud-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.add-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.2s;
}

.add-btn:hover {
  background: #2563eb;
}

.btn-icon {
  width: 1rem;
  height: 1rem;
}

.search-container {
  margin-bottom: 1.5rem;
}

.search-input-group {
  position: relative;
  max-width: 400px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1rem;
  height: 1rem;
  color: #9ca3af;
}

.search-input {
  width: 100%;
  padding: 0.75rem 0.75rem 0.75rem 2.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.search-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.table-container {
  overflow-x: auto;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th {
  background: #f9fafb;
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 1px solid #e5e7eb;
}

.table-row {
  transition: background 0.2s;
}

.table-row:hover {
  background: #f9fafb;
}

.data-table td {
  padding: 1rem;
  border-bottom: 1px solid #f3f4f6;
  color: #6b7280;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.edit-btn, .delete-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: background 0.2s;
}

.edit-btn {
  background: #f3f4f6;
  color: #374151;
}

.edit-btn:hover {
  background: #e5e7eb;
}

.delete-btn {
  background: #fef2f2;
  color: #dc2626;
}

.delete-btn:hover {
  background: #fee2e2;
}

.action-icon {
  width: 1rem;
  height: 1rem;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 1rem;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e5e7eb;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.close-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: background 0.2s;
}

.close-btn:hover {
  background: #f3f4f6;
}

.close-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: #374151;
}

.form-input {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  font-size: 0.875rem;
}

.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.cancel-btn {
  padding: 0.75rem 1.5rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  background: white;
  color: #374151;
  cursor: pointer;
  transition: background 0.2s;
}

.cancel-btn:hover {
  background: #f9fafb;
}

.save-btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  background: #10b981;
  color: white;
  cursor: pointer;
  transition: background 0.2s;
}

.save-btn:hover {
  background: #059669;
}
</style>
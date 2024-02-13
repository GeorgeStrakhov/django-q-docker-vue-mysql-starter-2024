<template>
  <div>
    <label :for="inputId" class="block text-900 font-medium mb-2">{{ label }}</label>
    <div>
      <InputText v-if="inputtype === 'inputtext'"
                 :id="inputId"
                 :modelValue="modelValue"
                 @update:modelValue="updateValue"
                 aria-describedby="help"
                 class="w-full mb-1"
                 :class="{ 'p-invalid': errors }"/>
      <Textarea v-else
                :id="inputId"
                :modelValue="modelValue"
                @update:modelValue="updateValue"
                aria-describedby="help"
                class="w-full mb-1"
                :class="{ 'p-invalid': errors }"/>
    </div>
    <div class="mt-0 mb-4">
      <small id="help" class="p-error">{{ errors }}</small>
    </div>
  </div>
</template>

<script>
import InputText from 'primevue/inputtext';
import Textarea from 'primevue/textarea';

export default {
    components: {
        InputText,
        Textarea,
    },
    props: {
        modelValue: [String, Number],
        inputtype: {
            type: String,
            default: 'inputtext', // or 'textarea'
        },
        label: String,
        errors: String,
        inputId: {
            type: String,
            required: true,
        },
    },
    emits: ['update:modelValue'],
    methods: {
        updateValue(value) {
            this.$emit('update:modelValue', value);
        },
    },
};
</script>

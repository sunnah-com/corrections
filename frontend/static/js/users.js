Vue.component('users-view', {
  props: ['token'],
  data: function () {
    return {
      gridInstance: null,
      users: [],
      search: '',
      isNewUserModal: true,
      showModalContent: false,
      username: '',
      selectedActions: [],
      allActions: [
        {
          id: "manage_users",
          text: "Manage users",
        },
        {
          id: "view_archive",
          text: "View archive",
        },
      ],
      selectedQueues: [],
      allQueues: [
        {
          id: "global",
          text: "Global",
        },
        {
          id: "secondary",
          text: "Secondary",
        },
      ],
    }
  },
  methods: {
    async getUsers() {
      this.users = await fetchJsonData(this.token, '/api/users');
    },
    handleEditUser(selectedUser = {}) {
      this.username = selectedUser.username;
      this.selectedActions = selectedUser.permissions.actions;
      this.selectedQueues = selectedUser.permissions.queues;
      this.isNewUserModal = false;
      this.showModalContent = true;
      $('#add-user-modal').modal('show');
    },
    async saveUser() {
      await fetchJsonData(this.token, '/api/users/' + this.username, {
        actions: this.selectedActions,
        queues: this.selectedQueues
      });
      this.closeModal();
    },
    closeModal() {
      this.isNewUserModal = true;
      this.showModalContent = false;
      this.username = '';
      this.selectedActions = []
      this.selectedQueues = [];
      $('#add-user-modal').modal('hide');
    },
  },
  computed: {
    usersData() {
      let users = this.users;
      users = users.filter(el => {
        if (el.username.toLowerCase().indexOf(this.search.toLowerCase()) != -1) {
          return true;
        }
      });
      return users;
    }
  },
  mounted: function () {
    const vm = this;
    vm.getUsers();
    $('#add-user-modal').on('hidden.bs.modal', function (event) {
      vm.closeModal();
    })
  }
})

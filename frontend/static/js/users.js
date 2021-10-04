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
      allQueues: []
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
    getQueues: async function () {
      try {
        const result = await fetchJsonData(this.token, '/api/queues/');
        this.allQueues = result.map(queue => ({
          id: queue["name"],
          text: queue["name"]
        }));
      }
      catch (err) {
        console.error("Failed to fetch queues:", err);
      }
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
    this.getUsers();
    this.getQueues();
    $('#add-user-modal').on('hidden.bs.modal', () => {
      this.closeModal();
    });
  }
})

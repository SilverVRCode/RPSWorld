<script setup></script>

<template>
  <div id="navbar">
    <div id="left-nav">
      <nav>
        <RouterLink to="/" id="title-text" class="nav-items">Scissors</RouterLink>
        <RouterLink to="about">About</RouterLink>
      </nav>
    </div>
    <div id="right-nav">

    </div>

  </div>
  <main>
    <router-view />
  </main>
</template>

<style scoped>
#navbar {
  height: 48px;
  width: 100%;
  display: flex;
  align-items: center;
  box-sizing: border-box;
  margin: 0;
  padding: 0 12px;
  position: sticky;
  top: 0;
  z-index: 1000;

  background-color: var(--secondary-color);
}

#navbar a {
  text-decoration: none;
  color: black;
}

.nav-items {
  margin: 0;
  line-height: 48px;
  padding: 4px;
}

#title-text {
  font-weight: 700;
  font-size: x-large;
  padding-right: 16px;
}
</style>

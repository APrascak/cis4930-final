context('Actions', () => {
	beforeEach(() => {
		cy.visit('http://localhost:3000/')
	})

	it('Attempts to sign up a user with valid password length', () => {
        let num = Math.round(Math.random() * 10000000)
        cy.visit('http://localhost:3000/signup')
		cy.get('input[name="username"]').type('test user')
        cy.get('input[name="email"]').type('test' + num + '@email.com')
        cy.get('input[name="passwordOne"]').type('longValidPassword')
        cy.get('input[name="passwordTwo"]').type('longValidPassword')
        cy.get('button').should('be.enabled')
		cy.get('form').submit()
		
		//Valid input should result in successful login to home panel
		cy.location('pathname').should('eq', '/home')
    })
    
})


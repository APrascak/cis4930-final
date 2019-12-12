describe('Sign in with invalid credentials for user', function() {
    context('Actions', () => {
	beforeEach(() => {
        cy.visit('http://localhost:3000/account')
	})

	it('Attempts to sign in user with invalid email', () => {
        cy.visit('http://localhost:3000/signin')
        cy.get('input[name="email"]').type('qwerty0987654321@mail.com')
        cy.get('input[name="password"]').type('password')
        cy.get('button').should('be.enabled')
        cy.get('button').click() 
        cy.contains('There is no user record corresponding to this identifier. The user may have been deleted.')
		
        cy.url().should('not.include', '/home')
    })

    it('Attempts to sign in user with invalid password', () => {
        cy.visit('http://localhost:3000/signin')
        cy.get('input[name="email"]').type('qwerty@mail.com')
        cy.get('input[name="password"]').type('invalidpassword')
        cy.get('button').should('be.enabled')
        cy.get('button').click() 
        cy.contains('The password is invalid or the user does not have a password.')
		
        cy.url().should('not.include', '/home')
    })
})
})

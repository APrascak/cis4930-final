

describe('HappyPath Test', function() {
    it('Tests signup', function() {
        var num = (Math.random()*10)
        cy.visit('http://localhost:3000/signup')

        cy.get('#username')
        .type('test')
        .should('have.value', 'test')

        cy.get('#email')
        .type(('testing'+ num + '@email.com'))
        .should('have.value', ('testing'+ num + '@email.com'))

        cy.get('#passwordOne')
        .type('testing12')
        .should('have.value', 'testing12')

        cy.get('#passwordTwo')
        .type('testing12')
        .should('have.value', 'testing12')

        cy.get('form').submit()
       

        cy.url().should('include', '/home')

    })
})
